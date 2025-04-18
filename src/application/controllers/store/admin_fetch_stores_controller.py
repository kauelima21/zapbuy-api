from application.schemas.store.admin_fetch_stores_schema import AdminFetchStoresSchema
from common.decorators import load_schema
from models.store import fetch_stores_by_owner


class AdminFetchStoresController:
    @staticmethod
    @load_schema(AdminFetchStoresSchema)
    def process(payload: dict) -> dict:
        owner_id = payload["request_context"]["authorizer"]["jwt"]["claims"]["sub"]

        stores = fetch_stores_by_owner(owner_id)

        return {
            "status_code": 200,
            "body": {
                "stores": [
                    {
                        "store_slug": store["store_slug"],
                        "owner_id": store["owner_id"],
                        "store_name": store["store_name"],
                        "whatsapp_number": store["whatsapp_number"],
                        "work_days": store["work_days"],
                        "work_hours": store["work_hours"],
                        "status": store["status"],
                        "created_at": str(store["created_at"]),
                        "updated_at": str(store["updated_at"]),
                    } for store in stores
                ]
            }
        }
