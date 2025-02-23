from application.schemas.store.find_store_schema import FindStoreSchema
from common.decorators import load_schema
from common.errors import NotFoundError
from models.store import find_store_by_slug


class FindStoreController:
    @staticmethod
    @load_schema(FindStoreSchema)
    def process(payload: dict) -> dict:
        store_slug = payload["params"]["slug"]

        store = find_store_by_slug(store_slug)

        if not store:
            raise NotFoundError("A loja solicitada não existe.")

        return {
            "status_code": 200,
            "body": {
                "store": {
                    "store_slug": store["store_slug"],
                    "owner_id": store["owner_id"],
                    "store_name": store["store_name"],
                    "whatsapp_number": store["whatsapp_number"],
                    "work_days": store["work_days"],
                    "work_hours": store["work_hours"],
                    "status": store["status"],
                }
            }
        }
