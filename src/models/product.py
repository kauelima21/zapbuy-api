from boto3.dynamodb.conditions import Key

from common.database import get_table


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
