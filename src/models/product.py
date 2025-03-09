import os

from boto3.dynamodb.conditions import Key
from nanoid import generate

from common.database import get_table
from common.s3 import generate_presigned_url


def find_product_by_store(product_id: str, store_slug: str):
    table = get_table()
    response = table.get_item(Key={
        "pk": f"PRODUCT#{product_id}",
        "sk": f"STORE#{store_slug}",
    })

    return response.get("Item")


def fetch_products_by_store(store_slug: str, filter_expression: str = None,
                            limit=None, last_key=None):
    table = get_table()
    query_params = {
        "IndexName": "gsi1",
        "KeyConditionExpression": Key("sk").eq(f"STORE#{store_slug}") & Key(
            "pk").begins_with(f"PRODUCT#"),
        "Limit": limit if limit else 50
    }

    if last_key:
        query_params["ExclusiveStartKey"] = last_key

    if filter_expression:
        query_params["FilterExpression"] = filter_expression

    return table.query(**query_params)


def save_product(payload: dict):
    table = get_table()

    payload["product_id"] = generate()

    table.put_item(
        Item={
            "pk": f"PRODUCT#{payload['product_id']}",
            "sk": f"STORE#{payload['store_slug']}",
            **payload,
        }
    )

    return payload["product_id"]


def generate_upload_url(store_slug: str, product_id: str, file_name: str, file_type: str):
    bucket_name = os.environ.get("ZAPBUY_BUCKET_NAME")
    file_extension = file_name.split(".")[-1]
    object_name = f"{store_slug}/{product_id}-{file_extension}"

    return generate_presigned_url(bucket_name, object_name, file_type)
