from boto3.dynamodb.conditions import Key, Attr

from application.schemas.fetch_store_products_schema import \
    FetchStoreProductsSchema
from common.database import get_table
from common.decorators import load_schema


class FetchStoreProductsController:
    @staticmethod
    @load_schema(FetchStoreProductsSchema)
    def process(payload):
        store_slug = payload["params"]["slug"]

        table = get_table()
        products = table.query(
            IndexName="gsi1",
            KeyConditionExpression=Key("sk").eq(f"STORE#{store_slug}")
            & Key("pk").begins_with(f"PRODUCT#"),
            FilterExpression=Attr("status").eq("active")
        )["Items"]

        return {"status_code": 200, "body": {"products": products}}
