from common.database import get_table


def find_user_by_id(user_id: str):
    table = get_table()
    response = table.get_item(Key={
        "pk": f"USER#{user_id}",
        "sk": f"USER#{user_id}",
    })

    return response.get("Item")
