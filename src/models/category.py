from boto3.dynamodb.conditions import Key

from common.database import get_table
from common.utils import remove_dict_keys, get_current_timestamp


def find_category_by_store(category_id: str, store_slug: str):
    table = get_table()
    response = table.query(KeyConditionExpression=Key("pk").eq(f"STORE#{store_slug}") & Key(
        "sk").eq(f"PRODUCT#{category_id}"))

    if len(response["Items"]) > 0:
        return response["Items"][0]


def fetch_categories_by_store(store_slug: str, filter_expression: str = None,
                              limit=None, last_key=None):
    table = get_table()
    query_params = {
        "KeyConditionExpression": Key("pk").eq(f"STORE#{store_slug}") & Key(
            "sk").begins_with("CATEGORY#"),
        "Limit": limit if limit else 50
    }

    if last_key:
        query_params["ExclusiveStartKey"] = last_key

    if filter_expression:
        query_params["FilterExpression"] = filter_expression

    return table.query(**query_params)


def save_category(payload: dict):
    table = get_table()

    table.put_item(
        Item={
            "pk": f"STORE#{payload['store_slug']}",
            "sk": f"CATEGORY#{payload['category_id']}",
            **payload,
            "created_at": get_current_timestamp(),
            "updated_at": get_current_timestamp(),
        }
    )

    return payload["category_id"]


def update_category(category: dict, return_values="UPDATED_NEW"):
    table = get_table()

    expression_values = {}
    expression_names = {}
    update_expression = []
    category_clone = category.copy()
    category_clone["updated_at"] = get_current_timestamp()
    key_items = remove_dict_keys(category_clone, ["pk", "sk"])
    for key, value in key_items.items():
        expression_values[f":{key}"] = value
        expression_names[f"#{key}"] = key
        update_expression.append(f"#{key} = :{key}")

    update_expression = "SET " + ", ".join(update_expression)

    return table.update_item(
        Key={"pk": category["pk"], "sk": category["sk"]},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values,
        ExpressionAttributeNames=expression_names,
        ReturnValues=return_values,
    )
