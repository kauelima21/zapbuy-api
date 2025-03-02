import json

from application.schemas.product.admin_fetch_store_products_schema import AdminFetchStoreProductsSchema
from common.decorators import load_schema
from common.errors import ForbiddenError
from models.product import fetch_products_by_store
from models.store import find_store_by_slug


class AdminFetchStoreProductsController:
    @staticmethod
    @load_schema(AdminFetchStoreProductsSchema)
    def process(payload: dict) -> dict:
        current_user = payload["request_context"]["authorizer"]["jwt"]["claims"]["sub"]
        store_slug = payload["params"]["slug"]
        store = find_store_by_slug(store_slug)

        if store["owner_id"] != current_user:
            raise ForbiddenError("Usuário não está autorizado a criar produtos nesta loja.")

        products = fetch_products_by_store(store_slug)

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
