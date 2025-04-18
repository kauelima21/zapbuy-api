from boto3.dynamodb.conditions import Attr

from application.schemas.store.find_store_schema import FindStoreSchema
from common.decorators import load_schema
from common.errors import NotFoundError
from common.utils import remove_dict_keys
from models.product import fetch_products_by_store
from models.store import find_store_by_slug


class FetchCategoriesController:
    @staticmethod
    @load_schema(FindStoreSchema)
    def process(payload: dict) -> dict:
        store_slug = payload["params"]["slug"]

        store = find_store_by_slug(store_slug)

        if not store:
            raise NotFoundError("A loja solicitada não existe.")

        response = fetch_products_by_store(store_slug, filter_expression=Attr("status").eq("active"))

        return {
            "status_code": 200,
            "body": {
                "categories": remove_dict_keys(
                    [{
                        **category,
                        "created_at": str(category["created_at"]),
                        "updated_at": str(category["updated_at"]),
                    } for category in response["Items"]], ["pk", "sk"]
                )
            },
        }
