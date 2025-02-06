from common.database import get_table


def find_user_by_id(user_id: str) -> dict:
    table = get_table()
    response = table.get_item(
        Key={
            "pk": f"USER#{user_id}",
            "sk": f"USER#{user_id}",
        }
    )

    return response.get("Item")


def save_user(payload: dict):
    table = get_table()
    response = table.put_item(
        Item={
            "pk": f"USER#{payload['user_id']}",
            "sk": f"USER#{payload['user_id']}",
            **payload,
        }
    )

    return response
