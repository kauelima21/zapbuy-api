from application.schemas.category.admin_fetch_categories_schema import (
    AdminFetchCategoriesSchema,
)
from common.decorators import load_schema
from common.errors import NotFoundError, ForbiddenError
from common.utils import remove_dict_keys
from models.category import fetch_categories_by_store
from models.store import find_store_by_slug


class AdminFetchCategoriesController:
    @staticmethod
    @load_schema(AdminFetchCategoriesSchema)
    def process(payload: dict) -> dict:
        owner_id = payload["request_context"]["authorizer"]["jwt"]["claims"]["sub"]
        store_slug = payload["params"]["slug"]

        store = find_store_by_slug(store_slug)

        if not store:
            raise NotFoundError("A loja solicitada não existe.")

        if store["owner_id"] != owner_id:
            raise ForbiddenError("Usuário não está autorizado a listar categorias nesta loja.")

        response = fetch_categories_by_store(store_slug)

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
