from application.schemas.find_product_schema import FindProductSchema
from common.decorators import load_schema
from models.product import find_product_by_store


class FindProduct:
    @staticmethod
    @load_schema(FindProductSchema)
    def process(payload):
        product_id = payload["params"]["product_id"]
        store_slug = payload["params"]["slug"]

        product = find_product_by_store(product_id, store_slug)

        if not product:
            return {"status_code": 410, "body": None}

        return {"status_code": 200, "body": {"product": product}}
