from application.schemas.category.update_category_schema import UpdateCategorySchema
from common.decorators import load_schema
from common.errors import NotFoundError, ConflictError, ForbiddenError
from models.category import find_category_by_store, update_category
from models.store import find_store_by_slug


class UpdateCategoryController:
    @staticmethod
    @load_schema(UpdateCategorySchema)
    def process(payload: dict) -> dict:
        owner_id = payload["request_context"]["authorizer"]["jwt"]["claims"]["sub"]
        store_slug = payload["params"]["slug"]
        category_id = payload["params"]["category_id"]
        category_name = payload["body"]["category_name"]
        category_status = payload["body"]["status"]

        store = find_store_by_slug(store_slug)

        if not store:
            raise NotFoundError("A loja solicitada não existe.")

        if store["owner_id"] != owner_id:
            raise ForbiddenError(
                "Usuário não está autorizado a editar categorias nesta loja."
            )

        category = find_category_by_store(category_id, store_slug)
        if not category:
            raise ConflictError("A categoria não está cadastrada.")

        category["category_name"] = category_name
        category["status"] = category_status
        update_category(category)

        return {
            "status_code": 201,
            "body": {"message": f"Categoria {category_id} atualizada com sucesso!"},
        }
