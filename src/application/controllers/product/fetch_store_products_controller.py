from boto3.dynamodb.conditions import Attr

from application.schemas.product.fetch_store_products_schema import \
    FetchStoreProductsSchema
from common.decorators import load_schema
from common.utils import remove_dict_keys
from models.product import fetch_products_by_store


class FetchStoreProductsController:
    @staticmethod
    @load_schema(FetchStoreProductsSchema)
    def process(payload: dict) -> dict:
        store_slug = payload["params"]["slug"]

        per_page = payload.get("query", {}).get("per_page")

        last_key = None
        last_pk = payload.get("query", {}).get("last_pk")
        last_sk = payload.get("query", {}).get("last_sk")

        if last_sk and last_pk:
            last_key = {"pk": last_pk, "sk": last_sk}

        response = fetch_products_by_store(
            store_slug, filter_expression=Attr("status").eq("active"),
            limit=per_page, last_key=last_key
        )

        return {
            "status_code": 200,
            "body": {
                "products": remove_dict_keys([
                    {
                        **product,
                        "price_in_cents": str(product["price_in_cents"]),
                        "created_at": str(product["created_at"]),
                        "updated_at": str(product["updated_at"]),
                    } for product in response["Items"]
                ], ["pk", "sk"]),
                "last_key": response.get("LastEvaluatedKey"),
            }
        }
