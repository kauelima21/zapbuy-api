import os
import uuid

from boto3.dynamodb.conditions import Key

from common.database import get_table
from common.s3 import generate_presigned_url


def find_product_by_store(product_id: str, store_slug: str):
    table = get_table()
    response = table.get_item(Key={
        "pk": f"PRODUCT#{product_id}",
        "sk": f"STORE#{store_slug}",
    })

    return response.get("Item")


def fetch_products_by_store(store_slug: str, filter_expression: str = None):
    table = get_table()
    query_params = {
        "IndexName": "gsi1",
        "KeyConditionExpression": Key("sk").eq(f"STORE#{store_slug}") & Key(
            "pk").begins_with(f"PRODUCT#")
    }

    if filter_expression:
        query_params["FilterExpression"] = filter_expression

    products = table.query(**query_params)["Items"]

    return products


def save_product(payload: dict):
    table = get_table()

    payload["product_id"] = str(uuid.uuid4())

    table.put_item(
        Item={
            "pk": f"PRODUCT#{payload['product_id']}",
            "sk": f"STORE#{payload['store_slug']}",
            **payload,
        }
    )

    return payload["product_id"]


def generate_upload_url(store_slug: str, product_id: str, file_name: str, file_type: str):
    product_image_key = uuid.uuid4()
    bucket_name = os.environ.get("ZAPBUY_BUCKET_NAME")
    object_name = f"{store_slug}/{product_id}/{product_image_key}-{file_name}"

    return generate_presigned_url(bucket_name, object_name, file_type)
