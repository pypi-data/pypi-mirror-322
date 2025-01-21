#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
# @Time    : 2024/12/19
# @Author  : liyutao01(liyutao01@baidu.com)
# @File    : create_deploy_job.py
"""
import bcelogger
import traceback
import yaml
import os
from argparse import ArgumentParser

from baidubce.exception import BceHttpClientError
from windmillclient.client.windmill_client import WindmillClient
from windmilltrainingv1.client.training_api_job import parse_job_name
from windmillmodelv1.client.model_api_modelstore import parse_modelstore_name
from windmillendpointv1.client.endpoint_api_deploy_job import get_template_parameters
from windmillendpointv1.client.endpoint_api import parse_endpoint_name
from windmillartifactv1.client.artifact_api_artifact import parse_artifact_name


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--model_store_name", required=False, type=str, default="")
    parser.add_argument("--endpoint_name", required=False, type=str, default="")
    parser.add_argument("--spec_name", required=False, type=str, default="")
    parser.add_argument("--job_name", required=False, type=str, default="")

    args, _ = parser.parse_known_args()
    return args


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

    endpoint_name = parse_endpoint_name(args.endpoint_name)
    job_name = parse_job_name(args.job_name)
    model_store_name = parse_modelstore_name(args.model_store_name)
    tags = {}

    # 从模型包 apply.yaml 中获取 ensemble 模型信息
    if not os.path.exists("apply.yaml"):
        tags = {
            "errorCode": "101",
            "errorMessage": "服务部署失败，文件格式错误：apply.yaml文件不存在！"
        }
        bcelogger.error(f"CreateDeployEndpointJob {args.job_name} Failed: apply.yaml file does not exist")
        windmill_client.update_job(workspace_id=job_name.workspace_id,
                                   project_name=job_name.project_name,
                                   local_name=job_name.local_name,
                                   tags=tags)
        return

    model_list = []
    with open('apply.yaml', 'r') as fb:
        for data in yaml.safe_load_all(fb):
            model_list.append(data)
    if len(model_list) == 0:
        tags = {
            "errorCode": "101",
            "errorMessage": "服务部署失败，文件格式错误：apply.yaml文件不存在模型信息！"
        }
        bcelogger.error(f"CreateDeployEndpointJob {args.job_name} Failed: apply.yaml does not have models information")
        windmill_client.update_job(workspace_id=job_name.workspace_id,
                                   project_name=job_name.project_name,
                                   local_name=job_name.local_name,
                                   tags=tags)
        return
    model_name = model_list[-1]["metadata"]["localName"]

    # 获取模型信息
    model = windmill_client.get_model(workspace_id=model_store_name.workspace_id,
                                      model_store_name=model_store_name.model_store_name,
                                      local_name=model_name.local_name)
    # 获取推荐配置信息
    # TODO: 添加盒子定制化启动参数
    template_parameters_map = get_template_parameters(model.preferModelServerParameters)

    # 部署预测服务
    spec_name = args.spec_name
    deployment_name = parse_artifact_name(spec_name)
    if deployment_name.version is None:
        spec_name = args.spec_name + "/versions/latest"
    try:
        windmill_client.create_deploy_endpoint_job(workspace_id=model_name.workspace_id,
                                                   endpoint_hub_name=endpoint_name.endpoint_hub_name,
                                                   endpoint_name=endpoint_name.local_name,
                                                   artifact_name=(args.model_store_name + "/models/" + model_name +
                                                                  "/versions/latest"),
                                                   spec_name=spec_name,
                                                   kind="Deploy",
                                                   template_parameters=template_parameters_map)
    except BceHttpClientError as bce_error:
        tags = {
            "errorCode": str(bce_error.last_error.status_code),
            "errorMessage": bce_error.last_error.args[0]
        }
        bcelogger.error(f"CreateDeployEndpointJob {args.job_name} Failed: {traceback.format_exc()}")
    except Exception as e:
        tags = {
            "errorCode": "400",
            "errorMessage": "服务部署失败，内部服务错误！"
        }
        bcelogger.error(f"CreateDeployEndpointJob {args.job_name} Failed: {traceback.format_exc()}")
    windmill_client.update_job(workspace_id=job_name.workspace_id,
                               project_name=job_name.project_name,
                               local_name=job_name.local_name,
                               tags=tags)


if __name__ == "__main__":
    run()
