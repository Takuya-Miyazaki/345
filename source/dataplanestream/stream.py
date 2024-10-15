# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import os
import boto3
import json
import decimal
from boto3.dynamodb.types import TypeDeserializer
from botocore import config
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

mie_config = json.loads(os.environ['botoConfig'])
config = config.Config(**mie_config)

ks = boto3.client('kinesis', config=config)
stream_name = os.environ['StreamName']
serializer = TypeDeserializer()


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


def deserialize(data):
    if isinstance(data, list):
        return [deserialize(v) for v in data]

    if isinstance(data, dict):
        try:
            return serializer.deserialize(data)
        except TypeError:
            return {k: deserialize(v) for k, v in data.items()}
    else:
        return data


def put_ks_record(pkey, data):
    ks.put_record(
        StreamName=stream_name,
        Data=json.dumps(data, cls=DecimalEncoder),
        PartitionKey=pkey,
    )


def diff_item_images(item_1, item_2):
    operators = []

    item_1_items = item_1.items()

    # Get attributes that store pointers
    for item in item_1_items:
        if isinstance(item[1], list):
            print("Adding the following to operator comparison list:", item)
            operators.append(item[0])

    # This could probably be a string, but keeping as a list for now until this design is tested
    modified_operator = []

    for operator in operators:
        item_1_pointer = item_1[operator][0]["pointer"]
        item_2_pointer = item_2[operator][0]["pointer"]

        print("Comparing:", item_1_pointer, "with:", item_2_pointer)

        if item_1_pointer != item_2_pointer:
            changed = {"operator": operator, "pointer": item_1_pointer, "workflow": item_1[operator][0]["workflow"]}
            print("Found the modified operator:", changed)
            modified_operator.append(changed)

    if len(modified_operator) > 1:
        # This really shouldn't happen, but adding just in case... see comment about storing as a string instead
        print("We somehow got modified pointers for more than one operator in one stream event")
    else:
        try:
            modified = modified_operator[0]
        except Exception as e:
            print("Unable to return the modified operator:", e)
        else:
            return modified


def determine_item_change(stream_record):
    new_item = stream_record["NewImage"]
    old_item = stream_record["OldImage"]

    new_attributes = set(new_item.keys())
    old_attributes = set(old_item.keys())

    # Check for new or removed attribute first
    if new_attributes == old_attributes:
        print("No attributes added or removed, this must be a modification on an existing attribute")
        modified_attribute = diff_item_images(new_item, old_item)
        return modified_attribute
    else:
        # Determine if new or removed
        new = new_attributes - old_attributes
        removed = old_attributes - new_attributes

        if new != set():
            new = str(list(new)[0])
            return {"operator": new, "pointer": new_item[new][0]["pointer"], "workflow": new_item[new][0]["workflow"]}
        if removed != set():
            removed = str(list(removed)[0])
            return {"operator": removed}


def build_metadata_object(stream_record, action):
    metadata_object = {}
    if action == "MODIFY":
        modified_attribute = determine_item_change(stream_record)
        if modified_attribute is None:
            print("Unable to determine modified operator")
        elif "pointer" not in modified_attribute:
            metadata_object["Action"] = "REMOVE"
            metadata_object["Operator"] = modified_attribute["operator"]
        else:
            metadata_object["Action"] = "MODIFY"
            metadata_object["Pointer"] = modified_attribute["pointer"]
            metadata_object["Operator"] = modified_attribute["operator"]
            metadata_object["Workflow"] = modified_attribute["workflow"]
    if action == "INSERT":
        items = stream_record["NewImage"]
        for item in items:
            if item != "AssetId":
                metadata_object[item] = items[item]
        metadata_object["Action"] = "INSERT"
    if action == "REMOVE":
        # For a delete we just need to pass the asset id and the action to remove
        metadata_object["Action"] = "REMOVE"

    if len(metadata_object) == 0:
        print("Unable to build metadata object")
        return {"Status": "Error"}
    else:
        print(metadata_object)
        return {"Status": "Success", "Results": metadata_object}


def lambda_handler(event, _context):
    print("Stream record received:", event)
    for record in event["Records"]:
        deserialized_record = deserialize(record["dynamodb"])
        print(deserialized_record)
        asset_id = deserialized_record["Keys"]["AssetId"]
        event_type = record["eventName"]
        if event_type in {"MODIFY", "INSERT", "REMOVE"}:
            metadata = build_metadata_object(deserialized_record, event_type)
            if metadata["Status"] == "Success":
                print('Putting the following data into the stream:', metadata["Results"])
                put_ks_record(asset_id, metadata["Results"])
            else:
                print("Nothing to put into stream")
