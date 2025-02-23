from application.schemas.product.fetch_store_products_schema import \
    FetchStoreProductsSchema
from common.decorators import load_schema
from models.product import fetch_products_by_store


class AdminFetchStoreProductsController:
    @staticmethod
    @load_schema(FetchStoreProductsSchema)
    def process(payload: dict) -> dict:
        store_slug = payload["params"]["slug"]

        products = fetch_products_by_store(store_slug)

        return {"status_code": 200, "body": {"products": products}}
