from application.schemas.product.product_action_schema import ProductActionSchema
from common.decorators import load_schema
from common.errors import ForbiddenError
from models.product import generate_upload_url
from models.store import find_store_by_slug


class ProductActionController:
    @staticmethod
    @load_schema(ProductActionSchema)
    def process(payload: dict) -> dict:
        current_user = payload["request_context"]["authorizer"]["jwt"]["claims"]["sub"]
        file_type = payload["body"]["file_type"]
        file_name = payload["body"]["file_name"]
        store_slug = payload["params"]["slug"]
        product_id = payload["params"]["product_id"]
        store = find_store_by_slug(store_slug)

        if store["owner_id"] != current_user:
            raise ForbiddenError("Usuário não está autorizado a modificar produtos nesta loja.")

        upload_url_response = generate_upload_url(store_slug, product_id, file_name, file_type)

        return {"status_code": 201, "body": upload_url_response}
