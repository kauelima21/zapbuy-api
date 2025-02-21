from application.schemas.save_store_schema import SaveStoreSchema
from common.decorators import load_schema
from common.errors import ConflictError
from common.utils import generate_slug
from models.store import save_store, find_store_by_slug


class SaveStoreController:
    @staticmethod
    @load_schema(SaveStoreSchema)
    def process(payload: dict) -> dict:
        store_payload = payload["body"]
        store_slug = generate_slug(store_payload["store_name"])

        store_payload["store_slug"] = store_slug

        has_store = find_store_by_slug(store_slug)

        if has_store:
            raise ConflictError("Já existe uma loja com esta slug.")

        save_store(store_payload)

        return {"status_code": 201, "body": None}
