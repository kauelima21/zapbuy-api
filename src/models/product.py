import os

from boto3.dynamodb.conditions import Key

from common.database import get_table
from common.s3 import generate_presigned_url
from common.utils import remove_dict_keys, get_current_timestamp


def find_product_by_store(product_id: str, store_slug: str):
    table = get_table()
    response = table.query(KeyConditionExpression=Key("pk").eq(f"STORE#{store_slug}") & Key(
            "sk").eq(f"PRODUCT#{product_id}"))

    if len(response["Items"]) > 0:
        return response["Items"][0]


def fetch_products_by_store(store_slug: str, filter_expression: str = None,
                            limit=None, last_key=None):
    table = get_table()
    query_params = {
        "KeyConditionExpression": Key("pk").eq(f"STORE#{store_slug}") & Key(
            "sk").begins_with("PRODUCT#"),
        "Limit": limit if limit else 50
    }

    if last_key:
        query_params["ExclusiveStartKey"] = last_key

    if filter_expression:
        query_params["FilterExpression"] = filter_expression

    return table.query(**query_params)


def save_product(payload: dict):
    from nanoid import generate

    table = get_table()

    payload["product_id"] = generate()

    table.put_item(
        Item={
            "pk": f"STORE#{payload['store_slug']}",
            "sk": f"PRODUCT#{payload['product_id']}",
            **payload,
            "created_at": get_current_timestamp(),
            "updated_at": get_current_timestamp(),
        }
    )

    return payload["product_id"]


def update_product(product: dict, return_values="UPDATED_NEW"):
    table = get_table()

    expression_values = {}
    expression_names = {}
    update_expression = []
    product_clone = product.copy()
    product_clone["updated_at"] = get_current_timestamp()
    key_items = remove_dict_keys(product_clone, ["pk", "sk"])
    for key, value in key_items.items():
        expression_values[f":{key}"] = value
        expression_names[f"#{key}"] = key
        update_expression.append(f"#{key} = :{key}")

    update_expression = "SET " + ", ".join(update_expression)

    return table.update_item(
        Key={"pk": product["pk"], "sk": product["sk"]},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values,
        ExpressionAttributeNames=expression_names,
        ReturnValues=return_values,
    )


def generate_upload_url(store_slug: str, product_id: str, file_name: str, file_type: str):
    bucket_name = os.environ.get("ZAPBUY_BUCKET_NAME")
    file_extension = file_name.split(".")[-1]
    object_name = f"{store_slug}/{product_id}.{file_extension}"

    presigned_url = generate_presigned_url(bucket_name, object_name, file_type)

    return {"url": presigned_url, "object_name": object_name}
