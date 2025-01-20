#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/9/10
# @Author  : zhangzhijun
# @File    : dump_model.py
"""
import os
from argparse import ArgumentParser

from jobv1.tracker.tracker import Tracker
from windmillartifactv1.client.artifact_api_artifact import parse_artifact_name
from windmillclient.client.windmill_client import WindmillClient
from windmillmodelv1.client.model_api_model import parse_model_name


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--artifact_name", required=True, type=str, default=""
                                                                            "workspaces/ws1/modelstores/ms1/models/m1/versions/1")
    parser.add_argument("--device_names",required=True,type=str,default="")
    args, _ = parser.parse_known_args()

    return args


def run():
    """
    sync model
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
    # prepare and check data
    artifact_name = parse_artifact_name(args.artifact_name)
    device_names = args.device_names.split(",")
    
    model_name = parse_model_name(artifact_name.object_name)
    model = windmill_client.get_model(model_name.workspace_id, model_name.model_store_name, model_name.local_name)
    device_list = windmill_client.list_device()

    tracker = Tracker(windmill_client=windmill_client, workspace_id=model_name.workspace_id)

if __name__ == "__main__":
    run()
