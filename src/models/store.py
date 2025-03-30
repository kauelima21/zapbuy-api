from boto3.dynamodb.conditions import Key

from common.database import get_table
from common.utils import get_current_timestamp, remove_dict_keys


def find_store_by_slug(store_slug: str):
    table = get_table()
    response = table.query(
        KeyConditionExpression=Key("pk").eq(f"STORE#{store_slug}") & Key(
            "sk").begins_with("OWNER#")
    )

    if len(response["Items"]) > 0:
        return response["Items"][0]

    return None


def fetch_stores_by_owner(owner_id: str):
    table = get_table()
    response = table.query(
        IndexName="gsi1",
        KeyConditionExpression=Key("sk").eq(f"OWNER#{owner_id}") & Key(
            "pk").begins_with("STORE#")
    )

    return response.get("Items")


def save_store(payload: dict):
    table = get_table()
    response = table.put_item(
        Item={
            "pk": f"STORE#{payload['store_slug']}",
            "sk": f"OWNER#{payload['owner_id']}",
            **payload,
            "created_at": get_current_timestamp(),
            "updated_at": get_current_timestamp(),
        }
    )

    return response


def update_store(store: dict, return_values="UPDATED_NEW"):
    table = get_table()

    expression_values = {}
    expression_names = {}
    update_expression = []
    store_clone = store.copy()
    store_clone["updated_at"] = get_current_timestamp()
    key_items = remove_dict_keys(store_clone, ["pk", "sk"])
    for key, value in key_items.items():
        expression_values[f":{key}"] = value
        expression_names[f"#{key}"] = key
        update_expression.append(f"#{key} = :{key}")

    update_expression = "SET " + ", ".join(update_expression)

    return table.update_item(
        Key={"pk": store["pk"], "sk": store["sk"]},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values,
        ExpressionAttributeNames=expression_names,
        ReturnValues=return_values,
    )
