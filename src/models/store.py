from boto3.dynamodb.conditions import Key

from common.database import get_table


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
