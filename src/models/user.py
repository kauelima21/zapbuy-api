from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from common.database import get_table
from common.utils import remove_dict_keys, get_current_timestamp


def find_user_by_id(user_id: str) -> dict | None:
    table = get_table()
    response = table.query(
        KeyConditionExpression=Key("pk").eq(f"USER#{user_id}") & Key(
            "sk").begins_with("USER#")
    )

    if response.get("Items") and len(response["Items"]) > 0:
        return response["Items"][0]

    return None


def find_user_by_email(email: str) -> dict | None:
    table = get_table()
    response = table.query(
        IndexName="gsi1",
        KeyConditionExpression=Key("sk").eq(f"USER#{email}") & Key(
            "pk").begins_with("USER#")
    )

    if response.get("Items") and len(response["Items"]) > 0:
        return response["Items"][0]

    return None


def update_user(user: dict, return_values="UPDATED_NEW"):
    table = get_table()

    expression_values = {}
    expression_names = {}
    update_expression = []
    user_clone = user.copy()
    user_clone["updated_at"] = get_current_timestamp()
    key_items = remove_dict_keys(user_clone, ["pk", "sk"])
    for key, value in key_items.items():
        expression_values[f":{key}"] = value
        expression_names[f"#{key}"] = key
        update_expression.append(f"#{key} = :{key}")

    update_expression = "SET " + ", ".join(update_expression)

    return table.update_item(
        Key={"pk": user["pk"], "sk": user["sk"]},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values,
        ExpressionAttributeNames=expression_names,
        ReturnValues=return_values,
    )


def save_user(payload: dict):
    table = get_table()
    response = table.put_item(
        Item={
            "pk": f"USER#{payload['user_id']}",
            "sk": f"USER#{payload['email']}",
            **payload,
            "created_at": get_current_timestamp(),
            "updated_at": get_current_timestamp(),
        }
    )

    return response
