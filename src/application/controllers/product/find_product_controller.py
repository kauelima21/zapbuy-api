import json

from application.schemas.product.find_product_schema import FindProductSchema
from common.constants import S3
from common.decorators import load_schema
from common.utils import remove_dict_keys
from models.product import find_product_by_store


class FindProductController:
    @staticmethod
    @load_schema(FindProductSchema)
    def process(payload: dict) -> dict:
        product_id = payload["params"]["product_id"]
        store_slug = payload["params"]["slug"]

        product = find_product_by_store(product_id, store_slug)

        if not product:
            return {"status_code": 410, "body": None}

        return {
            "status_code": 200,
            "body": {
                "product": remove_dict_keys({
                    **product,
                    "price_in_cents": int(product["price_in_cents"]),
                }, ["pk", "sk"])
            }
        }
