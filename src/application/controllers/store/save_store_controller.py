from application.schemas.store.save_store_schema import SaveStoreSchema
from common.decorators import load_schema
from common.errors import ConflictError
from common.utils import generate_slug
from models.store import save_store, find_store_by_slug


class SaveStoreController:
    @staticmethod
    @load_schema(SaveStoreSchema)
    def process(payload: dict) -> dict:
        current_user = payload["request_context"]["authorizer"]["jwt"]["claims"]["sub"]
        store_payload = payload["body"]
        store_slug = generate_slug(store_payload["store_name"])

        store_payload["store_slug"] = store_slug

        has_store = find_store_by_slug(store_slug)

        if has_store:
            raise ConflictError("Já existe uma loja com esta slug.")

        save_store({**store_payload, "owner_id": current_user, "status": "active"})

        return {"status_code": 201, "body": {"message": f"Loja {store_slug} criada com sucesso!"}}
