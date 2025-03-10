from application.schemas.product.admin_fetch_store_products_schema import AdminFetchStoreProductsSchema
from common.decorators import load_schema
from common.errors import ForbiddenError
from models.product import fetch_products_by_store, count_store_products
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

        per_page = payload.get("query", {}).get("per_page")

        last_key = None
        last_pk = payload.get("query", {}).get("last_pk")
        last_sk = payload.get("query", {}).get("last_sk")

        if last_sk and last_pk:
            last_key = {"pk": last_pk, "sk": last_sk}

        response = fetch_products_by_store(store_slug, limit=per_page, last_key=last_key)

        return {
            "status_code": 200,
            "body": {
                "products": [
                    {
                        "name": product["name"],
                        "description": product["description"],
                        "product_id": product["product_id"],
                        "store_slug": product["store_slug"],
                        "price_in_cents": str(product["price_in_cents"]),
                        "category": product["category"],
                        "status": product["status"],
                    }
                    for product in response["Items"]
                ],
                "last_key": response.get("LastEvaluatedKey"),
                "total": count_store_products(store_slug)
            },
        }
