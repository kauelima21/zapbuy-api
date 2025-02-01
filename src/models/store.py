from common.database import get_table


def find_store_by_slug(store_slug: str):
    table = get_table()
    response = table.get_item(Key={
        "pk": f"STORE#{store_slug}",
        "sk": f"STORE#{store_slug}",
    })

    return response.get("Item")
