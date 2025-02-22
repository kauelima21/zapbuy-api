import json

from application.schemas.save_product_schema import SaveProductSchema
from common.decorators import load_schema
from common.errors import ValidationError, ForbiddenError
from models.product import save_product
from models.store import find_store_by_slug


class SaveProductController:
    @staticmethod
    @load_schema(SaveProductSchema)
    def process(payload: dict) -> dict:
        current_user = payload["request_context"]["authorizer"]["claims"]["sub"]
        store_slug = payload["params"]["slug"]
        store = find_store_by_slug(store_slug)
        body = payload["body"]

        if not store:
            raise ValidationError("A loja informada não foi encontrada.")

        if store["owner_id"] != current_user:
            raise ForbiddenError("Usuário não está autorizado a criar produtos nesta loja.")

        body["price_in_cents"] = int(body["price_in_cents"]),
        body["categories"] = json.dumps(body["categories"])
        product_id = save_product({**body, "store_slug": store_slug})

        return {"status_code": 201, "body": {"product_id": product_id}}
