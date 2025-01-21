#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
# @Time    : 2024/12/19
# @Author  : liyutao01(liyutao01@baidu.com)
# @File    : import_deploy_skill.py
"""

import bcelogger
import os
import re
import shutil
import subprocess
import time
import traceback
import yaml

from argparse import ArgumentParser

from baidubce.exception import BceHttpClientError
from bceinternalsdk.client.paging import PagingRequest
from windmillclient.client.windmill_client import WindmillClient
from windmillcomputev1.filesystem import download_by_filesystem
from windmilltrainingv1.client.training_api_job import parse_job_name
from windmillmodelv1.client.model_api_modelstore import parse_modelstore_name
from windmillcategoryv1.client.category_api import match
from windmillmodelv1.client.model_api_model import Category
from windmillendpointv1.client.endpoint_api_deploy_job import get_template_parameters
from windmillendpointv1.client.endpoint_api import parse_endpoint_name
from windmillendpointv1.client.endpoint_api_deployment import parse_deployment_name
from windmillartifactv1.client.artifact_api_artifact import parse_artifact_name
from windmillmodelv1.client.model_api_model import parse_model_name
from windmillmodelv1.client.model_api_model import PreferModelServerParameters

from tritonv2.model_config import ModelConfig
from tritonv2.utils import BlobStoreFactory

DEBUG = True


def _delete_model_file(path):
    """
    删除指定 artifact 的模型文件
    """

    try:
        if os.path.exists(path):
            shutil.rmtree(path)
    except OSError as e:
        return False
    return True


def _process_location(location):
    """
    修正location
    e.g. "/data/model/workspaces/wsvykgec/modelstores/ms-4B6vVufC/models/model1/1-1735485337987"
        => "/data/model/workspaces/wsvykgec/modelstores/ms-4B6vVufC/models/model1/1"
    """
    location_dir = os.path.dirname(location)
    location_basename = os.path.basename(location)
    pattern = r'^(\d+)-(\d{10,})$'

    parts = re.match(pattern, location_basename)

    if parts:
        return os.path.join(location_dir, parts.group(1))
    else:
        return location


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
    parser.add_argument("--model_base_path", required=False, type=str, default="/data/model")

    args, _ = parser.parse_known_args()
    return args


def import_models(args, windmill_client):
    """
     导入模型包, 包括原子模型 artifact 去重
    """
    ret_artifact_list = []  # 导入的原子模型 artifact 列表
    model_info = {}  # key = 原子模型 localName, value = {"version": "1", "location": "xxx"}

    model_store = parse_modelstore_name(args.model_store_name)
    job_name = parse_job_name(args.job_name)
    tags = {}

    # 构建远端 filesystem
    # fs_remote = {
    #     "host": os.getenv("SOURCE_HOST", ""),
    #     "kind": os.getenv("SOURCE_KIND", ""),
    #     "endpoint": os.getenv("SOURCE_ENDPOINT", ""),
    #     "credential": {
    #         "accessKey": os.getenv("SOURCE_ACCESS_KEY", ""),
    #         "secretKey": os.getenv("SOURCE_SECRET_KEY", ""),
    #     },
    #     "config": {
    #         "disableSSL": os.getenv("SOURCE_DISABLE_SSL", ""),
    #         "region": os.getenv("SOURCE_REGION", ""),
    #     }
    # }
    fs_remote = {
        "host": "10.27.240.45:8455",
        "kind": "s3",
        "endpoint": "windmill/store/68b4691df5fd48a7a23742fed8d39c36",
        "credential": {
            "accessKey": "AKIAIOSFODNN7EXAMPLE",
            "secretKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        },
        "config": {
            "disableSSL": "true",
            "region": "bj",
        }
    }

    # 1. 下载 apply.yaml 文件
    file_name = "apply.yaml"
    try:
        if args.uri.startswith("http"):
            cmd = ['curl', '-o', file_name, args.uri]
            subprocess.run(cmd, shell=False, check=True)
        elif args.uri.startswith("/") or args.uri.startswith("."):
            shutil.copyfile(args.uri, file_name)
        else:
            file_name = os.path.basename(args.uri)
            download_by_filesystem(fs_remote, args.uri, file_name)
    except Exception as e:
        tags = {
            "errorCode": "102",
            "errorMessage": "模型 apply.yaml 路径有误：uri不存在！"
        }
        bcelogger.error(f"ImportDeploySkillJob {args.job_name} Failed: {traceback.format_exc()}")
        if not DEBUG:
            windmill_client.update_job(workspace_id=job_name.workspace_id,
                                       project_name=job_name.project_name,
                                       local_name=job_name.local_name,
                                       tags=tags)
        return None
    # 判断 apply.yaml 文件是否成功下载
    if not os.path.exists(file_name):
        tags = {
            "errorCode": "101",
            "errorMessage": "文件格式错误：apply.yaml文件不存在！"
        }
        bcelogger.error(f"ImportDeploySkillJob {args.job_name} Failed: apply.yaml file does not exist")
        if not DEBUG:
            windmill_client.update_job(workspace_id=job_name.workspace_id,
                                       project_name=job_name.project_name,
                                       local_name=job_name.local_name,
                                       tags=tags)
        return None

    # 2. 解析、下载、创建模型, 并将模型文件按照 triton 规范 copy 到宿主机的指定位置
    model_list = []
    with open('apply.yaml', 'r') as fb:
        for data in yaml.safe_load_all(fb):
            tags[data["metadata"]["localName"]] = ""
            model_list.append(data)
    if not DEBUG:
        windmill_client.update_job(workspace_id=job_name.workspace_id,
                                   project_name=job_name.project_name,
                                   local_name=job_name.local_name,
                                   tags=tags)
    print("model_list_len = ", len(model_list))
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
            # 先将模型文件 copy 到宿主机fs, 避免出现model artifact 已经创建但是没有模型文件的情况
            location = windmill_client.create_location(object_name=(args.model_store_name + "/models/" +
                                                       model["metadata"]["localName"]),
                                                       style="Triton")
            dest_path = _process_location(location.location)
            # 直接从远端 fs copy 到本地 fs
            download_by_filesystem(fs_remote, model["metadata"]["artifact"]["uri"], dest_path)

            # 按照 triton 标准调整宿主机上的模型文件
            for file_name in os.listdir(dest_path):
                src_file = dest_path + "/" + file_name
                if os.path.isdir(src_file):
                    continue
                if file_name.endswith(".yaml") or file_name.endswith(".yml") or file_name.endswith(".pbtxt"):
                    dest_file = os.path.abspath(dest_path + "/../" + file_name)
                    shutil.copyfile(src_file, dest_file)

            # 创建模型
            resp = windmill_client.create_model(
                workspace_id=model_store.workspace_id,
                model_store_name=model_store.local_name,
                local_name=model["metadata"]["localName"],
                display_name=model["metadata"]["displayName"],
                prefer_model_server_parameters=model["metadata"]["preferModelServerParameters"],
                # category=model["metadata"]["category"],
                category="Other",
                model_formats=model["metadata"]["modelFormats"],
                artifact_tags=model["metadata"]["artifact"]["tags"],
                artifact_metadata=model["metadata"]["artifact"]["metadata"],
                # "file" 开头, 并且盒子上 filesystem 类型为 "file", 不会再次执行模型文件上传操作
                artifact_uri=("file://" + dest_path))

            # 记录每个 artifact 的信息
            ret_artifact_list.append(resp.artifact)

            # if match(model["metadata"]["category"], Category.CategoryImageEnsemble.value):
            #     sub_model_list = windmill_client.get_model_manifest(model_store.workspace_id,
            #                                                         model_store.local_name,
            #                                                         resp.localName,
            #                                                         str(resp.artifact["version"]))
            #     for item in sub_model_list.subModels:
            #         tags[item["localName"]] = str(item["artifact"]["version"])
    except BceHttpClientError as bce_error:
        tags = {
            "errorCode": str(bce_error.last_error.status_code),
            "errorMessage": bce_error.last_error.args[0]
        }
        bcelogger.error(f"ImportDeploySkillJob {args.job_name} Failed: {traceback.format_exc()}")
        if not DEBUG:
            windmill_client.update_job(workspace_id=job_name.workspace_id,
                                       project_name=job_name.project_name,
                                       local_name=job_name.local_name,
                                       tags=tags)
        return None
    except Exception as e:
        tags = {
            "errorCode": "400",
            "errorMessage": "内部服务错误, 下载模型文件出错！"
        }
        bcelogger.error(f"ImportDeploySkillJob {args.job_name} Failed: {traceback.format_exc()}")
        if not DEBUG:
            windmill_client.update_job(workspace_id=job_name.workspace_id,
                                       project_name=job_name.project_name,
                                       local_name=job_name.local_name,
                                       tags=tags)
        return None

    # 设置 ensemble 节点中依赖的子模型包版本
    # 将子模型版本信息保存到 ensemble 节点的 config.pbtxt 中
    bs = BlobStoreFactory.create(kind="local", bucket="", endpoint_url="")
    for artifact in ret_artifact_list:
        info = {}
        artifact_name = parse_artifact_name(artifact["name"])
        model_name = parse_model_name(artifact_name.object_name)
        info["version"] = str(artifact["version"])
        info["location"] = artifact["uri"].replace("file://", "")
        model_info[model_name.local_name] = info
    print("model_version_len = ", len(model_info))
    for name, info in model_info.items():
        sub_model_path = info["location"]
        config = ModelConfig.create_from_file(os.path.join(sub_model_path, "config.pbtxt"))
        if not config.is_ensemble():
            continue
        step = config.get_ensemble_steps()
        for sub_model_name, sub_model_info in step.items():
            if sub_model_name not in model_info.keys():
                tags = {
                    "errorCode": "400",
                    "errorMessage": f"缺少原子模型 {sub_model_name}！"
                }
                bcelogger.error(f"ImportDeploySkillJob {args.job_name} Failed: sub model {sub_model_name} is missing!")
                if not DEBUG:
                    windmill_client.update_job(workspace_id=job_name.workspace_id,
                                               project_name=job_name.project_name,
                                               local_name=job_name.local_name,
                                               tags=tags)
                return None
            config.set_scheduling_model_version(sub_model_name, model_info[sub_model_name]["version"])
        print("sub_model_path = ", sub_model_path)
        config.write_to_file(os.path.join(sub_model_path, "config.pbtxt"), bs)
        config.write_to_file(os.path.join(sub_model_path, "../", "config.pbtxt"), bs)
    if not DEBUG:
        windmill_client.update_job(workspace_id=job_name.workspace_id,
                                   project_name=job_name.project_name,
                                   local_name=job_name.local_name,
                                   tags=tags)
    return ret_artifact_list


def create_deploy_job(args, model_artifact, windmill_client):
    """
    创建预测服务部署任务, 并检查部署状态
    """
    success = False
    endpoint_name = parse_endpoint_name(args.endpoint_name)
    job_name = parse_job_name(args.job_name)
    artifact_name = parse_artifact_name(model_artifact["name"])
    model_name = parse_model_name(artifact_name.object_name)
    tags = {}

    try:
        model = windmill_client.get_model(workspace_id=model_name.workspace_id,
                                          model_store_name=model_name.model_store_name,
                                          local_name=model_name.local_name)
    except BceHttpClientError as bce_error:
        tags = {
            "errorCode": str(bce_error.last_error.status_code),
            "errorMessage": bce_error.last_error.args[0]
        }
        bcelogger.error(f"ImportDeploySkillJob {args.job_name} Failed: {traceback.format_exc()}")
        if DEBUG:
            windmill_client.update_job(workspace_id=job_name.workspace_id,
                                       project_name=job_name.project_name,
                                       local_name=job_name.local_name,
                                       tags=tags)
        return success
    except Exception as e:
        tags = {
            "errorCode": "400",
            "errorMessage": f"部署服务失败，无法获取 {model_name.local_name} 模型信息！"
        }
        bcelogger.error(f"ImportDeploySkillJob {args.job_name} Failed: {traceback.format_exc()}")
        if DEBUG:
            windmill_client.update_job(workspace_id=job_name.workspace_id,
                                       project_name=job_name.project_name,
                                       local_name=job_name.local_name,
                                       tags=tags)
        return success

    # 获取模型推荐配置信息
    # TODO: 添加盒子定制化启动参数
    parameters = PreferModelServerParameters(**model.preferModelServerParameters)
    template_parameters_map = get_template_parameters(parameters)
    print("template_parameters_map = ", template_parameters_map)

    # 获取计算资源信息
    accelerator = ""
    endpoint_compute_name = ""
    spec_name = args.spec_name
    deployment_artifact_name = parse_artifact_name(spec_name)
    if deployment_artifact_name.version is None:
        spec_name = args.spec_name + "/versions/latest"
    deployment_artifact_name = parse_artifact_name(spec_name)
    deployment_name = parse_deployment_name(deployment_artifact_name.object_name)

    # if model.preferModelServerParameters.resource.accelerator:
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
            tags = {
                "errorCode": str(bce_error.last_error.status_code),
                "errorMessage": bce_error.last_error.args[0]
            }
            bcelogger.error(f"ImportDeploySkillJob {args.job_name} Failed: {traceback.format_exc()}")
            if DEBUG:
                windmill_client.update_job(workspace_id=job_name.workspace_id,
                                           project_name=job_name.project_name,
                                           local_name=job_name.local_name,
                                           tags=tags)
            return success
        except Exception as e:
            tags = {
                "errorCode": "400",
                "errorMessage": "部署服务失败，无法获取计算资源！"
            }
            bcelogger.error(f"ImportDeploySkillJob {args.job_name} Failed: {traceback.format_exc()}")
            if DEBUG:
                windmill_client.update_job(workspace_id=job_name.workspace_id,
                                           project_name=job_name.project_name,
                                           local_name=job_name.local_name,
                                           tags=tags)
            return success
    # 获取计算资源列表, 如果没有指定计算资源，则使用第一个计算资源
    guest_name = "workspaces/" + endpoint_name.workspace_id + "/endpointhubs/" + endpoint_name.endpoint_hub_name
    try:
        compute_list = windmill_client.suggest_compute(workspace_id=endpoint_name.workspace_id,
                                                       guest_name=guest_name)
        # print("compute_list = ", compute_list)
        for compute in compute_list.computes:
            if (("tags" in compute) and ("accelerator" in compute["tags"]) and
                    (compute["tags"]["accelerator"] == accelerator)):
                endpoint_compute_name = compute["name"]
                print("hello t4")
                break
        if endpoint_compute_name == "":
            if len(compute_list.computes) > 0:
                endpoint_compute_name = compute_list.computes[0]["name"]
            else:
                tags = {
                    "errorCode": "400",
                    "errorMessage": "部署服务失败，无法获取计算资源！"
                }
                bcelogger.error(f"ImportDeploySkillJob {args.job_name} Failed: {traceback.format_exc()}")
                windmill_client.update_job(workspace_id=job_name.workspace_id,
                                           project_name=job_name.project_name,
                                           local_name=job_name.local_name,
                                           tags=tags)
                return success
    except BceHttpClientError as bce_error:
        tags = {
            "errorCode": str(bce_error.last_error.status_code),
            "errorMessage": bce_error.last_error.args[0]
        }
        bcelogger.error(f"ImportDeploySkillJob {args.job_name} Failed: {traceback.format_exc()}")
        windmill_client.update_job(workspace_id=job_name.workspace_id,
                                   project_name=job_name.project_name,
                                   local_name=job_name.local_name,
                                   tags=tags)
        return success
    except Exception as e:
        tags = {
            "errorCode": "400",
            "errorMessage": "部署服务失败，无法获取计算资源！"
        }
        bcelogger.error(f"ImportDeploySkillJob {args.job_name} Failed: {traceback.format_exc()}")
        windmill_client.update_job(workspace_id=job_name.workspace_id,
                                   project_name=job_name.project_name,
                                   local_name=job_name.local_name,
                                   tags=tags)
        return success

    # 部署预测服务
    try:
        windmill_client.create_deploy_endpoint_job(workspace_id=endpoint_name.workspace_id,
                                                   endpoint_hub_name=endpoint_name.endpoint_hub_name,
                                                   endpoint_name=endpoint_name.local_name,
                                                   # artifact_name=model_artifact["name"],
                                                   artifact_name="workspaces/wsvykgec/modelstores/ms-NxuYIVjg/models/modelXAydPBtr-T4-ensemble/versions/2",
                                                   spec_name=spec_name,
                                                   endpoint_compute_name=endpoint_compute_name,
                                                   kind="Deploy",
                                                   template_parameters=template_parameters_map)
    except BceHttpClientError as bce_error:
        tags = {
            "errorCode": str(bce_error.last_error.status_code),
            "errorMessage": bce_error.last_error.args[0]
        }
        bcelogger.error(f"ImportDeploySkillJob {args.job_name} Failed: {traceback.format_exc()}")
        windmill_client.update_job(workspace_id=job_name.workspace_id,
                                   project_name=job_name.project_name,
                                   local_name=job_name.local_name,
                                   tags=tags)
        return success
    except Exception as e:
        tags = {
            "errorCode": "400",
            "errorMessage": "服务部署失败，内部服务错误！"
        }
        bcelogger.error(f"ImportDeploySkillJob {args.job_name} Failed: {traceback.format_exc()}")
        windmill_client.update_job(workspace_id=job_name.workspace_id,
                                   project_name=job_name.project_name,
                                   local_name=job_name.local_name,
                                   tags=tags)
        return success

    # 检查部署状态
    for i in range(0, 90):
        print("start new loop")
        time.sleep(10)
        try:
            status = windmill_client.get_endpoint_status(workspace_id=endpoint_name.workspace_id,
                                                         endpoint_hub_name=endpoint_name.endpoint_hub_name,
                                                         local_name=endpoint_name.local_name)
            print("status.deploymentStatus = ", status.deploymentStatus)
            print("i = ", i)
            if status.deploymentStatus == "Completed":
                success = True
                break
            elif status.deploymentStatus == "Failed":
                tags = {
                    "errorCode": "400",
                    "errorMessage": "服务部署失败，内部服务错误！"
                }
                bcelogger.error(f"ImportDeploySkillJob {args.job_name} Failed: {traceback.format_exc()}")
                if DEBUG:
                    windmill_client.update_job(workspace_id=job_name.workspace_id,
                                               project_name=job_name.project_name,
                                               local_name=job_name.local_name,
                                               tags=tags)
                return success
        except BceHttpClientError as bce_error:
            tags = {
                "errorCode": str(bce_error.last_error.status_code),
                "errorMessage": bce_error.last_error.args[0]
            }
            bcelogger.error(f"ImportDeploySkillJob {args.job_name} Failed: {traceback.format_exc()}")
            if DEBUG:
                windmill_client.update_job(workspace_id=job_name.workspace_id,
                                           project_name=job_name.project_name,
                                           local_name=job_name.local_name,
                                           tags=tags)
            return success
        except Exception as e:
            tags = {
                "errorCode": "400",
                "errorMessage": "服务部署失败，无法获取服务状态！"
            }
            bcelogger.error(f"ImportDeploySkillJob {args.job_name} Failed: {traceback.format_exc()}")
            if DEBUG:
                windmill_client.update_job(workspace_id=job_name.workspace_id,
                                           project_name=job_name.project_name,
                                           local_name=job_name.local_name,
                                           tags=tags)
            return success
        print("again")
    return success


def delete_models(args, model_artifact_list, windmill_client):
    """
    删除历史模型包, 只保留最新的两个版本和正在使用的版本
    :param args:
    :param model_artifact_list: 新部署的模型 artifact 列表
    :param windmill_client:
    :return:
    """

    try:
        for model_artifact in model_artifact_list:
            artifact_name = parse_artifact_name(model_artifact["name"])
            artifacts = windmill_client.list_artifact(object_name=artifact_name.object_name,
                                                      page_request=PagingRequest(page_no=1, page_size=100,
                                                                                 order="desc", orderby="version"))

            if artifacts.totalCount <= 1:
                continue
            total_count = artifacts.totalCount
            processed_count = len(artifacts.result)
            for i in range(1, len(artifacts.result)):
                if str(artifacts.result[i]["version"]) != str(model_artifact["version"]):
                    windmill_client.delete_artifact(object_name=artifact_name.object_name,
                                                    version=str(artifacts.result[i]["version"]))
                    location = artifacts.result[i]["uri"].replace("file://", "")
                    if not _delete_model_file(location):
                        bcelogger.error(f"DeleteModels Failed: {traceback.format_exc()}")

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
                        if not _delete_model_file(location):
                            bcelogger.error(f"DeleteModels Failed: {traceback.format_exc()}")
    except Exception as e:
        bcelogger.error(f"DeleteModels Failed: {traceback.format_exc()}")

    print("Delete models success.")

def run():
    """
    create deploy endpoint job
    """
    args = parse_args()
    # org_id = os.getenv("ORG_ID", "")
    # user_id = os.getenv("USER_ID", "")
    # windmill_endpoint = os.getenv("WINDMILL_ENDPOINT", "")
    # windmill_client = WindmillClient(endpoint=windmill_endpoint,
    #                                  context={"OrgID": org_id, "UserID": user_id})
    windmill_ak = "1cb1860b8bc848298050edffa2ef9e16"
    windmill_sk = "51a7a74c9ef14063a6892d08dd19ffbf"
    org_id = "07e17c96439e4d5da9f9c9817e1d2ad5"
    user_id = "9b70ba591c554c28ae5b311f794a238c"
    windmill_endpoint = "10.27.240.43:8342"
    windmill_client = WindmillClient(endpoint=windmill_endpoint,
                                     context={"OrgID": org_id, "UserID": user_id})

    # ret = windmill_client.create_location(object_name="workspaces/wsvykgec/modelstores/ms-4B6vVufC/models/model1",
    #                                       style="Triton")
    # print(ret)
    # location = ret.location
    # print("location = ", location)
    # print("成功")
    # return

    # 1. 导入模型包, 包括将模型包保存到盒子fs(盒子本地固定路径)
    model_artifact_list = import_models(args, windmill_client)
    if (model_artifact_list is None) or (len(model_artifact_list) == 0):
        print("No model found.")
        return
    print("Import models success.")
    # # 2. 服务部署/更新
    ensemble_model = model_artifact_list[-1]  # 对于 triton 模型包, 最后一个模型包就是 ensemble model
    deploy_success = create_deploy_job(args, ensemble_model, windmill_client)

    # # 3. 删除历史模型包
    # # 新模型部署成功, 删除历史模型， 只保留最新的两个版本和正在使用的版本
    # if deploy_success:
    #     delete_models(args, model_artifact_list, windmill_client)


if __name__ == "__main__":
    run()
