#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
# @Time    : 2025/01/07
# @Author  : liyutao01(liyutao01@baidu.com)
# @File    : import_deploy_model.py
"""

import bcelogger
import os
import subprocess
import time
import traceback
import yaml

from argparse import ArgumentParser

from baidubce.exception import BceHttpClientError
from bceinternalsdk.client.paging import PagingRequest
from jobv1.client.job_client import JobClient
from jobv1.client.job_api_event import CreateEventRequest
from jobv1.client.job_api_event import EventKind
from jobv1.client.job_api_job import parse_job_name
from windmillclient.client.windmill_client import WindmillClient
from windmillcomputev1.filesystem import download_by_filesystem, delete_by_filesystem
from windmillmodelv1.client.model_api_modelstore import parse_modelstore_name
from windmillendpointv1.client.endpoint_api_deploy_job import get_template_parameters
from windmillendpointv1.client.endpoint_api import parse_endpoint_name
from windmillendpointv1.client.endpoint_api_deployment import parse_deployment_name
from windmillartifactv1.client.artifact_api_artifact import parse_artifact_name
from windmillmodelv1.client.model_api_model import parse_model_name
from windmillmodelv1.client.model_api_model import PreferModelServerParameters

from tritonv2.model_config import ModelConfig
from tritonv2.utils import BlobStoreFactory


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--uri", required=False, type=str, default="")
    parser.add_argument("--model_store_name", required=False, type=str, default="")
    parser.add_argument("--endpoint_name", required=False, type=str, default="")
    parser.add_argument("--spec_name", required=False, type=str, default="")
    parser.add_argument("--job_name", required=False, type=str, default="")

    args, _ = parser.parse_known_args()
    return args


def import_models(args, windmill_client, job_client, fs_local):
    """
     导入模型包, 包括原子模型 artifact 去重
    """
    ret_artifact_list = []  # 导入的原子模型 artifact 列表
    model_info = {}  # key = 原子模型 localName, value = {"version": "1", "location": "xxx"}

    model_store = parse_modelstore_name(args.model_store_name)
    job_name = parse_job_name(args.job_name)
    create_task_event_req = CreateEventRequest(
        workspace_id=job_name.workspace_id,
        job_name=job_name.local_name,
        task_name="task-import-model",
        kind=EventKind.Succeed,
        reason="模型导入成功",
        message="模型包成功创建并导入本地 filesystem")

    # 构建远端 filesystem
    fs_remote = {
        "host": os.getenv("SOURCE_HOST", ""),
        "kind": os.getenv("SOURCE_KIND", ""),
        "endpoint": os.getenv("SOURCE_ENDPOINT", ""),
        "credential": {
            "accessKey": os.getenv("SOURCE_ACCESS_KEY", ""),
            "secretKey": os.getenv("SOURCE_SECRET_KEY", ""),
        },
        "config": {
            "disableSSL": os.getenv("SOURCE_DISABLE_SSL", ""),
            "region": os.getenv("SOURCE_REGION", ""),
        }
    }

    # 1. 下载 apply.yaml 文件
    file_name = "apply.yaml"
    try:
        if args.uri.startswith("http"):
            cmd = ['curl', '-o', file_name, args.uri]
            subprocess.run(cmd, shell=False, check=True)
        elif args.uri.startswith("/") or args.uri.startswith("."):  # local
            file_name = args.uri
        else:  # remote s3
            file_name = os.path.basename(args.uri)
            download_by_filesystem(fs_remote, args.uri, file_name)
    except Exception as e:
        create_task_event_req.kind = EventKind.Failed
        create_task_event_req.reason = "模型 apply.yaml 路径有误: uri不存在"
        create_task_event_req.message = "模型导入失败，模型 apply.yaml 路径有误"
        bcelogger.error(f"ImportDeployModelJob {args.job_name} Failed: {traceback.format_exc()}")
        job_client.create_event(create_task_event_req)
        return None

    # 判断 apply.yaml 文件是否成功下载
    if not os.path.exists(file_name):
        create_task_event_req.kind = EventKind.Failed
        create_task_event_req.reason = "模型 apply.yaml 文件不存在"
        create_task_event_req.message = "模型导入失败，模型 apply.yaml 文件不存在"
        bcelogger.error(f"ImportDeployModelJob {args.job_name} Failed: apply.yaml file does not exist")
        job_client.create_event(create_task_event_req)
        return None

    # 2. 解析、下载、创建模型
    model_list = []
    with open(file_name, 'r') as fb:
        for data in yaml.safe_load_all(fb):
            model_list.append(data)

    try:
        for model in model_list:
            # 2.1 判断模型 artifact 是否已经存在, 已经存在的模型 artifact 不重复下载
            is_saved = False
            source_version = model.get("metadata", {}).get("artifact", {}).get("tags", {}).get("sourceVersion", "")
            artifacts = windmill_client.list_artifact(object_name=(args.model_store_name + "/models/" +
                                                                   model["metadata"]["localName"]),
                                                      page_request=PagingRequest(page_no=1, page_size=100,
                                                                                 order="desc", orderby="version"))
            total_count = artifacts.totalCount
            processed_count = len(artifacts.result)
            for artifact in artifacts.result:
                if artifact.get("tags", {}).get("sourceVersion", "") == source_version:
                    ret_artifact_list.append(artifact)
                    is_saved = True
                    break
            while (not is_saved) and (processed_count < total_count):
                artifacts = windmill_client.list_artifact(object_name=(args.model_store_name + "/models/" +
                                                                       model["metadata"]["localName"]),
                                                          page_request=PagingRequest(page_no=1, page_size=100,
                                                                                     order="desc", orderby="version"))
                processed_count += len(artifacts.result)
                for artifact in artifacts.result:
                    if artifact.get("tags", {}).get("sourceVersion", "") == source_version:
                        ret_artifact_list.append(artifact)
                        is_saved = True
                        break
                if is_saved:
                    break
            if is_saved:
                continue

            # 2.2 下载没有下载过的模型 model/artifact
            # 创建模型
            resp = windmill_client.create_model(
                workspace_id=model_store.workspace_id,
                model_store_name=model_store.local_name,
                local_name=model["metadata"]["localName"],
                display_name=model["metadata"]["displayName"],
                prefer_model_server_parameters=model["metadata"]["preferModelServerParameters"],
                category=model["metadata"]["category"],
                model_formats=model["metadata"]["modelFormats"],
                artifact_tags=model["metadata"]["artifact"]["tags"],
                artifact_metadata=model["metadata"]["artifact"]["metadata"],
                artifact_uri=model["metadata"]["artifact"]["uri"],
                style="Triton",
                filesystem_remote=fs_remote)

            # 记录每个 artifact 的信息
            ret_artifact_list.append(resp.artifact)

    except BceHttpClientError as bce_error:
        create_task_event_req.kind = EventKind.Failed
        create_task_event_req.reason = f"无法创建模型: {bce_error.last_error.args[0]}"
        create_task_event_req.message = f"模型导入失败，无法创建模型: {bce_error.last_error.args[0]}"
        bcelogger.error(f"ImportDeployModelJob {args.job_name} Failed: {traceback.format_exc()}")
        job_client.create_event(create_task_event_req)
        return None
    except Exception as e:
        create_task_event_req.kind = EventKind.Failed
        create_task_event_req.reason = "无法创建模型, 内部服务错误"
        create_task_event_req.message = "模型导入失败, 无法创建模型, 内部服务错误"
        bcelogger.error(f"ImportDeployModelJob {args.job_name} Failed: {traceback.format_exc()}")
        job_client.create_event(create_task_event_req)
        return None

    # 导入的模型包不能为空
    if len(ret_artifact_list) == 0:
        create_task_event_req.kind = EventKind.Failed
        create_task_event_req.reason = "无法创建模型, 导入模型包为空"
        create_task_event_req.message = "模型导入失败, 无法创建模型, 导入模型包为空"
        bcelogger.error(f"ImportDeployModelJob {args.job_name} Failed: the models package is empty")
        job_client.create_event(create_task_event_req)
        return None

    # 3. 设置 ensemble 节点中依赖的子模型包版本, 只对 file 类型的 filesystem 有效, s3 类型的直接使用最新版子模型
    if fs_local["kind"] == "file":
        # 将子模型版本信息保存到 ensemble 节点的 config.pbtxt 中
        bs = BlobStoreFactory.create(kind="local", bucket="", endpoint_url="")
        for artifact in ret_artifact_list:
            info = {}
            artifact_name = parse_artifact_name(artifact["name"])
            model_name = parse_model_name(artifact_name.object_name)
            info["version"] = str(artifact["version"])
            info["location"] = artifact["uri"].replace("file://", "")
            model_info[model_name.local_name] = info
        for name, info in model_info.items():
            sub_model_path = info["location"]
            config = ModelConfig.create_from_file(os.path.join(sub_model_path, "config.pbtxt"))
            if not config.is_ensemble():
                continue
            step = config.get_ensemble_steps()
            for sub_model_name, sub_model_info in step.items():
                if sub_model_name not in model_info.keys():
                    create_task_event_req.kind = EventKind.Failed
                    create_task_event_req.reason = f"缺少原子模型 {sub_model_name}"
                    create_task_event_req.message = f"模型导入失败, 缺少原子模型 {sub_model_name}"
                    bcelogger.error(f"ImportDeployModelJob {args.job_name} Failed: sub model {sub_model_name} is missing!")
                    job_client.create_event(create_task_event_req)
                    return None
                config.set_scheduling_model_version(sub_model_name, model_info[sub_model_name]["version"])
            config.write_to_file(os.path.join(sub_model_path, "config.pbtxt"), bs)

    # 模型导入任务成功, 更新 task 状态
    job_client.create_event(create_task_event_req)

    return ret_artifact_list


def create_deploy_job(args, model_artifact, windmill_client, job_client):
    """
    创建预测服务部署任务, 并检查部署状态
    """
    success = False
    endpoint_name = parse_endpoint_name(args.endpoint_name)
    job_name = parse_job_name(args.job_name)
    artifact_name = parse_artifact_name(model_artifact["name"])
    model_name = parse_model_name(artifact_name.object_name)

    create_task_event_req = CreateEventRequest(
        workspace_id=job_name.workspace_id,
        job_name=job_name.local_name,
        task_name="task-create-deploy",
        kind=EventKind.Succeed,
        reason="服务部署成功",
        message="更改部署/更新预测服务")

    # 1. 获取模型推荐配置信息
    try:
        model = windmill_client.get_model(workspace_id=model_name.workspace_id,
                                          model_store_name=model_name.model_store_name,
                                          local_name=model_name.local_name)
    except BceHttpClientError as bce_error:
        create_task_event_req.kind = EventKind.Failed
        create_task_event_req.reason = f"无法获取模型信息: {bce_error.last_error.args[0]}"
        create_task_event_req.message = f"服务部署失败, 无法获取模型信息: {bce_error.last_error.args[0]}"
        bcelogger.error(f"ImportDeployModelJob {args.job_name} Failed: {traceback.format_exc()}")
        job_client.create_event(create_task_event_req)

        return success
    except Exception as e:
        create_task_event_req.kind = EventKind.Failed
        create_task_event_req.reason = f"部署服务失败，无法获取 {model_name.local_name} 模型信息"
        create_task_event_req.message = f"部署服务失败，无法获取 {model_name.local_name} 模型信息"
        bcelogger.error(f"ImportDeployModelJob {args.job_name} Failed: {traceback.format_exc()}")
        job_client.create_event(create_task_event_req)
        return success

    # TODO: 添加盒子定制化启动参数
    parameters = PreferModelServerParameters(**model.preferModelServerParameters)
    template_parameters_map = get_template_parameters(parameters)

    # 2. 获取计算资源信息
    accelerator = ""
    endpoint_compute_name = ""
    spec_name = args.spec_name
    deployment_artifact_name = parse_artifact_name(spec_name)
    if deployment_artifact_name.version is None:
        spec_name = args.spec_name + "/versions/latest"
    deployment_artifact_name = parse_artifact_name(spec_name)
    deployment_name = parse_deployment_name(deployment_artifact_name.object_name)

    if model.preferModelServerParameters.get("resource", {}).get("accelerator", "") != "":
        accelerator = model.preferModelServerParameters["resource"]["accelerator"]
    else:
        # 从 deployment 里面拿 accelerator
        try:
            manifest = windmill_client.get_deployment_manifest(workspace_id=deployment_name.workspace_id,
                                                               endpoint_hub_name=deployment_name.endpoint_hub_name,
                                                               endpoint_name=deployment_name.local_name,
                                                               version=deployment_artifact_name.version)
            resource = manifest.Capabilities.get("Values", {}).get("resource", {})
            if resource and ("accelerator" in resource):
                accelerator = resource["accelerator"]
        except BceHttpClientError as bce_error:
            create_task_event_req.kind = EventKind.Failed
            create_task_event_req.reason = f"无法获取 accelerator 信息: {bce_error.last_error.args[0]}"
            create_task_event_req.message = f"服务部署失败, 无法获取 accelerator 信息: {bce_error.last_error.args[0]}"
            bcelogger.error(f"ImportDeployModelJob {args.job_name} Failed: {traceback.format_exc()}")
            job_client.create_event(create_task_event_req)
            return success
        except Exception as e:
            create_task_event_req.kind = EventKind.Failed
            create_task_event_req.reason = "无法获取 accelerator 信息"
            create_task_event_req.message = "服务部署失败, 无法获取 accelerator 信息"
            bcelogger.error(f"ImportDeployModelJob {args.job_name} Failed: {traceback.format_exc()}")
            job_client.create_event(create_task_event_req)
            return success

    # 获取计算资源列表, 如果没有指定计算资源，则使用第一个计算资源
    guest_name = "workspaces/" + endpoint_name.workspace_id + "/endpointhubs/" + endpoint_name.endpoint_hub_name
    try:
        compute_list = windmill_client.suggest_compute(workspace_id=endpoint_name.workspace_id,
                                                       guest_name=guest_name)
        for compute in compute_list.computes:
            if (("tags" in compute) and ("accelerator" in compute["tags"]) and
                    (compute["tags"]["accelerator"] == accelerator)):
                endpoint_compute_name = compute["name"]
                break
        if endpoint_compute_name == "":
            if len(compute_list.computes) > 0:
                endpoint_compute_name = compute_list.computes[0]["name"]
            else:
                create_task_event_req.kind = EventKind.Failed
                create_task_event_req.reason = "无法获取计算资源"
                create_task_event_req.message = "服务部署失败, 无法获取计算资源"
                bcelogger.error(f"ImportDeployModelJob {args.job_name} Failed: {traceback.format_exc()}")
                job_client.create_event(create_task_event_req)
                return success
    except BceHttpClientError as bce_error:
        create_task_event_req.kind = EventKind.Failed
        create_task_event_req.reason = f"无法获取计算资源: {bce_error.last_error.args[0]}"
        create_task_event_req.message = f"服务部署失败, 无法获取计算资源: {bce_error.last_error.args[0]}"
        bcelogger.error(f"ImportDeployModelJob {args.job_name} Failed: {traceback.format_exc()}")
        job_client.create_event(create_task_event_req)
        return success
    except Exception as e:
        create_task_event_req.kind = EventKind.Failed
        create_task_event_req.reason = "无法获取计算资源"
        create_task_event_req.message = "服务部署失败, 无法获取计算资源"
        bcelogger.error(f"ImportDeployModelJob {args.job_name} Failed: {traceback.format_exc()}")
        job_client.create_event(create_task_event_req)
        return success

    # 3. 部署预测服务
    try:
        windmill_client.create_deploy_endpoint_job(workspace_id=endpoint_name.workspace_id,
                                                   endpoint_hub_name=endpoint_name.endpoint_hub_name,
                                                   endpoint_name=endpoint_name.local_name,
                                                   artifact_name=model_artifact["name"],
                                                   spec_name=spec_name,
                                                   endpoint_compute_name=endpoint_compute_name,
                                                   kind="Deploy",
                                                   template_parameters=template_parameters_map)
    except BceHttpClientError as bce_error:
        create_task_event_req.kind = EventKind.Failed
        create_task_event_req.reason = f"无法创建部署任务: {bce_error.last_error.args[0]}"
        create_task_event_req.message = f"服务部署失败, 无法创建部署任务: {bce_error.last_error.args[0]}"
        bcelogger.error(f"ImportDeployModelJob {args.job_name} Failed: {traceback.format_exc()}")
        job_client.create_event(create_task_event_req)
        return success
    except Exception as e:
        create_task_event_req.kind = EventKind.Failed
        create_task_event_req.reason = "无法创建部署任务"
        create_task_event_req.message = "服务部署失败, 无法创建部署任务"
        bcelogger.error(f"ImportDeployModelJob {args.job_name} Failed: {traceback.format_exc()}")
        job_client.create_event(create_task_event_req)
        return success

    # 4. 检查部署状态, timeout = 15min
    for i in range(0, 15):
        time.sleep(60)
        try:
            status = windmill_client.get_endpoint_status(workspace_id=endpoint_name.workspace_id,
                                                         endpoint_hub_name=endpoint_name.endpoint_hub_name,
                                                         local_name=endpoint_name.local_name)
            if status.deploymentStatus == "Completed":
                success = True
                break
            elif status.deploymentStatus == "Failed":
                create_task_event_req.kind = EventKind.Failed
                create_task_event_req.reason = "预测服务实例状态异常"
                create_task_event_req.message = "服务部署失败, 预测服务实例状态异常"
                bcelogger.error(f"ImportDeployModelJob {args.job_name} Failed: {traceback.format_exc()}")
                job_client.create_event(create_task_event_req)
                return success
        except BceHttpClientError as bce_error:
            create_task_event_req.kind = EventKind.Failed
            create_task_event_req.reason = f"无法获取预测服务实例状态: {bce_error.last_error.args[0]}"
            create_task_event_req.message = f"服务部署失败, 无法获取预测服务实例状态: {bce_error.last_error.args[0]}"
            bcelogger.error(f"ImportDeployModelJob {args.job_name} Failed: {traceback.format_exc()}")
            job_client.create_event(create_task_event_req)
            return success
        except Exception as e:
            create_task_event_req.kind = EventKind.Failed
            create_task_event_req.reason = "无法获取预测服务实例状态"
            create_task_event_req.message = "服务部署失败, 无法获取预测服务实例状态"
            bcelogger.error(f"ImportDeployModelJob {args.job_name} Failed: {traceback.format_exc()}")
            job_client.create_event(create_task_event_req)
            return success

    # 服务部署任务成功, 更新 task 状态
    job_client.create_event(create_task_event_req)
    return success


def delete_models(args, model_artifact_list, windmill_client, job_client, fs_local):
    """
    删除历史模型包, 只保留最新的两个版本和正在使用的版本
    """
    job_name = parse_job_name(args.job_name)
    create_task_event_req = CreateEventRequest(
        workspace_id=job_name.workspace_id,
        job_name=job_name.local_name,
        task_name="task-delete-previous-models",
        kind=EventKind.Succeed,
        reason="删除历史模型成功",
        message="删除历史模型成功")

    try:
        for model_artifact in model_artifact_list:
            artifact_name = parse_artifact_name(model_artifact["name"])
            artifacts = windmill_client.list_artifact(object_name=artifact_name.object_name,
                                                      page_request=PagingRequest(page_no=1, page_size=100,
                                                                                 order="desc", orderby="version"))

            if artifacts.totalCount <= 2:
                continue
            total_count = artifacts.totalCount
            processed_count = len(artifacts.result)
            for i in range(2, len(artifacts.result)):
                if str(artifacts.result[i]["version"]) != str(model_artifact["version"]):
                    windmill_client.delete_artifact(object_name=artifact_name.object_name,
                                                    version=str(artifacts.result[i]["version"]))
                    location = artifacts.result[i]["uri"].replace("file://", "")
                    delete_by_filesystem(fs_local, location)
            while processed_count < total_count:
                artifacts = windmill_client.list_artifact(object_name=artifact_name.object_name,
                                                          page_request=PagingRequest(page_no=1, page_size=100,
                                                                                     order="asc", orderby="version"))
                processed_count += len(artifacts.result)
                for artifact in artifacts.result:
                    if str(artifact["version"]) != str(model_artifact["version"]):
                        windmill_client.delete_artifact(object_name=artifact_name.object_name,
                                                        version=str(artifact.version))
                        location = artifact["uri"].replace("file://", "")
                        delete_by_filesystem(fs_local, location)
    except Exception as e:
        create_task_event_req.kind = EventKind.Failed
        create_task_event_req.reason = "无法获取预测服务实例状态"
        create_task_event_req.message = "服务部署失败, 无法获取预测服务实例状态"
        bcelogger.error(f"DeleteModels Failed: {traceback.format_exc()}")
        job_client.create_event(create_task_event_req)
        return

    # 删除历史模型任务成功, 更新 task 状态
    job_client.create_event(create_task_event_req)


def run():
    """
    create deploy endpoint job
    """
    args = parse_args()
    org_id = os.getenv("ORG_ID", "")
    user_id = os.getenv("USER_ID", "")
    windmill_endpoint = os.getenv("WINDMILL_ENDPOINT", "")
    windmill_client = WindmillClient(endpoint=windmill_endpoint,
                                     context={"OrgID": org_id, "UserID": user_id})

    job_client = JobClient(endpoint=windmill_endpoint,
                           context={"OrgID": org_id, "UserID": user_id})
    # 构建本地 filesystem
    fs_local = {
        "host": os.getenv("LOCAL_HOST", ""),
        "kind": os.getenv("LOCAL_KIND", ""),
        "endpoint": os.getenv("LOCAL_ENDPOINT", ""),
        "credential": {
            "accessKey": os.getenv("LOCAL_ACCESS_KEY", ""),
            "secretKey": os.getenv("LOCAL_SECRET_KEY", ""),
        },
        "config": {
            "disableSSL": os.getenv("LOCAL_DISABLE_SSL", ""),
            "region": os.getenv("LOCAL_REGION", ""),
        }
    }

    # 1. 导入模型包, 包括将模型包保存到本地fs(盒子本地固定路径)
    model_artifact_list = import_models(args, windmill_client, job_client, fs_local)
    if (model_artifact_list is None) or (len(model_artifact_list) == 0):
        return

    # 2. 服务部署/更新
    ensemble_model = model_artifact_list[-1]  # 对于 triton 模型包, 最后一个模型包就是 ensemble model
    deploy_success = create_deploy_job(args, ensemble_model, windmill_client, job_client)

    # 3. 删除历史模型包
    # 新模型部署成功, 删除历史模型， 只保留最新的两个版本和正在使用的版本
    if deploy_success:
        delete_models(args, model_artifact_list, windmill_client, job_client, fs_local)

    # 4. 删除 apply.yaml 文件
    delete_by_filesystem(fs_local, args.uri)


if __name__ == "__main__":
    run()
