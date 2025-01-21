#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2025/01/19
# @Author  : liyutao
# @File    : delete_previous_model.py
"""
import os
import requests
import time
import traceback

from argparse import ArgumentParser

import bcelogger

from baidubce.exception import BceHttpClientError
from bceinternalsdk.client.paging import PagingRequest
from windmillartifactv1.client.artifact_api_artifact import parse_artifact_name
from windmillclient.client.windmill_client import WindmillClient
from windmillmodelv1.client.model_api_model import parse_model_name


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--model_name", required=False, type=str, default="")
    parser.add_argument("--readiness_probe",
                        required=False,
                        type=str,
                        default="http://localhost:8080/v2/health/ready")
    parser.add_argument("--failure_threshold",
                        required=False,
                        type=int,
                        default=20)
    parser.add_argument("--period_seconds",
                        required=False,
                        type=int,
                        default=10)
    parser.add_argument("--timeout_seconds",
                        required=False,
                        type=int,
                        default=5)

    args, _ = parser.parse_known_args()

    return args


def is_ready(readiness_probe, timeout_seconds):
    """
    check if the pod is ready.
    """
    try:
        response = requests.get(url=readiness_probe, timeout=timeout_seconds)
        return response.status_code == 200
    except requests.ConnectionError:
        return False


def delete_previous_model(windmill_client, artifact_name):
    """
    删除历史模型包, 只保留最新的两个版本和正在使用的版本
    """
    name = parse_artifact_name(artifact_name)
    model_name = parse_model_name(name.object_name)

    manifest_list = windmill_client.get_model_manifest(model_name.workspace_id,
                                                       model_name.model_store_name,
                                                       model_name.local_name,
                                                       name.version)
    try:
        for model in manifest_list.subModels:
            # 兼容一个模型包中有多个 ensemble 节点的情况
            if model["localName"] != model_name.local_name:
                delete_previous_model(windmill_client, model["artifact"]["name"])
            page_no = 1
            artifacts = windmill_client.list_artifact(object_name=model["name"],
                                                      page_request=PagingRequest(page_no=page_no, page_size=100,
                                                                                 order="desc", orderby="version"))
            page_no += 1
            if artifacts.totalCount <= 2:
                continue
            total_count = artifacts.totalCount
            processed_count = len(artifacts.result)
            for i in range(2, len(artifacts.result)):
                if str(artifacts.result[i]["version"]) != str(model["artifact"]["version"]):
                    sub_artifact_name = parse_artifact_name(artifacts.result[i]["name"])
                    windmill_client.delete_artifact(object_name=sub_artifact_name.object_name,
                                                    version=sub_artifact_name.version,
                                                    force=True)
            while processed_count < total_count:
                artifacts = windmill_client.list_artifact(object_name=artifact_name.object_name,
                                                          page_request=PagingRequest(page_no=page_no, page_size=100,
                                                                                     order="asc", orderby="version"))
                page_no += 1
                processed_count += len(artifacts.result)
                for artifact in artifacts.result:
                    if str(artifact["version"]) != str(model["artifact"]["version"]):
                        sub_artifact_name = parse_artifact_name(artifact["name"])
                        windmill_client.delete_artifact(object_name=sub_artifact_name.object_name,
                                                        version=sub_artifact_name.version,
                                                        force=True)
    except BceHttpClientError as bce_error:
        bcelogger.error(f"DeleteModels Failed: {bce_error.last_error.args[0]}")
        return
    except Exception as e:
        bcelogger.error(f"DeleteModels Failed: {traceback.format_exc()}")
        return


def run():
    """
    服务部署成功后删除历史模型包
    """
    args = parse_args()
    org_id = os.getenv("ORG_ID", "")
    user_id = os.getenv("USER_ID", "")
    windmill_endpoint = os.getenv("WINDMILL_ENDPOINT", "")
    windmill_client = WindmillClient(endpoint=windmill_endpoint,
                                     context={
                                         "OrgID": org_id,
                                         "UserID": user_id
                                     })
    model_name = args.model_name

    # 检查当前 pod 是否已经正常运行
    readied = False
    for i in range(args.failure_threshold):
        readied = is_ready(args.readiness_probe, args.timeout_seconds)
        if readied:
            break
        else:
            time.sleep(args.period_seconds)

    if not readied:
        bcelogger.error("pod is not ready, don't delete previous model.")
        return

    delete_previous_model(windmill_client, model_name)


if __name__ == "__main__":
    run()
