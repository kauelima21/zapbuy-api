import json
import os

import boto3


def get_file_extension(product_keys: list):
    file_type = product_keys[1].split(".")[1]

    if file_type == "jpg":
        file_type = "jpeg"

    return file_type


def handler(event: dict, _):
    records = event["Records"]

    for record in records:
        object_key = record["s3"]["object"]["key"]
        product_keys = object_key.split("/")
        store_slug = product_keys[0]
        product_id = product_keys[1].split(".")[0]
        file_type = get_file_extension(product_keys)

        sqs_client = boto3.client('sqs')
        sqs_client.send_message(
            QueueUrl=os.environ.get("ZAPBUY_IMAGES_QUEUE_RULE"),
            MessageBody=json.dumps({
                "object_key": object_key,
                "store_slug": store_slug,
                "product_id": product_id,
                "file_type": file_type
            })
        )

    return {"status_code": 204, "body": None}
