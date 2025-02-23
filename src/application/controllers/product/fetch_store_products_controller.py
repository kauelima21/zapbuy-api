import json

from boto3.dynamodb.conditions import Attr

from application.schemas.product.fetch_store_products_schema import \
    FetchStoreProductsSchema
from common.decorators import load_schema
from models.product import fetch_products_by_store


class FetchStoreProductsController:
    @staticmethod
    @load_schema(FetchStoreProductsSchema)
    def process(payload: dict) -> dict:
        store_slug = payload["params"]["slug"]

        products = fetch_products_by_store(store_slug,
                                           Attr("status").eq("active"))

        return {
            "status_code": 200,
            "body": {
                "products": [
                    {
                        "name": product["name"],
                        "description": product["description"],
                        "product_id": product["product_id"],
                        "store_slug": product["store_slug"],
                        "price_in_cents": int(product["price_in_cents"]),
                        "categories": json.loads(product["categories"]),
                        "status": product["status"],
                    } for product in products
                ]
            }
        }
