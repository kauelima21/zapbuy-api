from application.schemas.admin_fetch_stores_schema import AdminFetchStoresSchema
from common.decorators import load_schema
from models.store import fetch_stores_by_owner


class AdminFetchStoresController:
    @staticmethod
    @load_schema(AdminFetchStoresSchema)
    def process(payload):
        owner_id = payload["params"]["owner_id"]

        stores = fetch_stores_by_owner(owner_id)

        return {"status_code": 200, "body": {"stores": stores}}
