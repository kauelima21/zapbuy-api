from application.schemas.product.update_product_schema import UpdateProductSchema
from common.decorators import load_schema
from common.errors import ValidationError, ForbiddenError
from models.product import find_product_by_store, update_product
from models.store import find_store_by_slug


class UpdateProductController:
    @staticmethod
    @load_schema(UpdateProductSchema)
    def process(payload: dict) -> dict:
        current_user = payload["request_context"]["authorizer"]["jwt"]["claims"]["sub"]
        store_slug = payload["params"]["slug"]
        product_id = payload["params"]["product_id"]
        store = find_store_by_slug(store_slug)
        body = payload["body"]

        if not store:
            raise ValidationError("A loja informada não foi encontrada.")

        if store["owner_id"] != current_user:
            raise ForbiddenError("Usuário não está autorizado a criar produtos nesta loja.")

        product = find_product_by_store(product_id, store_slug)
        product["name"] = body["name"]
        product["description"] = body["description"]
        product["price_in_cents"] = body["price_in_cents"]
        product["category"] = body["category"]
        product["status"] = body["status"]

        update_product(product)

        return {
            "status_code": 200,
            "body": {"message": "Produto atualizado com sucesso."},
        }
