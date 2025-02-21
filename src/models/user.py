from boto3.dynamodb.conditions import Key

from common.database import get_table


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


def save_user(payload: dict):
    table = get_table()
    response = table.put_item(
        Item={
            "pk": f"USER#{payload['user_id']}",
            "sk": f"USER#{payload['email']}",
            **payload,
        }
    )

    return response
