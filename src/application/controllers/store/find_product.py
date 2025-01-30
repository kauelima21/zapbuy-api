from application.schemas.find_product_schema import FindProductSchema
from common.database import get_table
from common.decorators import load_schema


class FindProduct:
    @staticmethod
    @load_schema(FindProductSchema)
    def process(payload):
        product_id = payload["params"]["product_id"]
        store_slug = payload["params"]["slug"]

        table = get_table()
        product = table.get_item(Key={
            "pk": f"PRODUCT#{product_id}",
            "sk": f"STORE#{store_slug}",
        })

        if not product.get("Item"):
            return {"status_code": 410, "body": None}

        return {"status_code": 200, "body": {"product": product["Item"]}}
