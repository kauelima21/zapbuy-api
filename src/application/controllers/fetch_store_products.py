from boto3.dynamodb.conditions import Key

from application.schemas.fetch_store_products_schema import \
    FetchStoreProductsSchema
from common.database import get_table
from common.decorators import load_schema


@load_schema(FetchStoreProductsSchema)
def process(payload):
    store_slug = payload["params"]["store_slug"]

    table = get_table()
    products = table.query(
        IndexName="gsi1",
        KeyConditionExpression=Key("sk").eq(f"STORE#{store_slug}")
        & Key("pk").begins_with(f"PRODUCT#")
    )["Items"]

    return products
