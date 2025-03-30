from application.schemas.category.save_category_schema import SaveCategorySchema
from common.decorators import load_schema
from common.errors import NotFoundError, ConflictError, ForbiddenError
from common.utils import generate_slug
from models.category import find_category_by_store, save_category
from models.store import find_store_by_slug


class SaveCategoryController:
    @staticmethod
    @load_schema(SaveCategorySchema)
    def process(payload: dict) -> dict:
        owner_id = payload["request_context"]["authorizer"]["jwt"]["claims"]["sub"]
        store_slug = payload["params"]["slug"]
        category_name = payload["body"]["category_name"]

        store = find_store_by_slug(store_slug)

        if not store:
            raise NotFoundError("A loja solicitada não existe.")

        if store["owner_id"] != owner_id:
            raise ForbiddenError(
                "Usuário não está autorizado a criar categorias nesta loja."
            )

        category_slug = generate_slug(category_name)
        has_category = find_category_by_store(category_slug, store_slug)
        if has_category:
            raise ConflictError("A categoria já está cadastrada.")

        save_category(
            {
                "category_id": category_slug,
                "category_name": category_name,
                "store_slug": store_slug,
                "status": "active",
            }
        )

        return {
            "status_code": 201,
            "body": {"message": f"Categoria {category_slug} criada com sucesso!"},
        }
