from application.schemas.find_store_schema import FindStoreSchema
from common.database import get_table
from common.decorators import load_schema


class FindStore:
    @staticmethod
    @load_schema(FindStoreSchema)
    def process(payload):
        store_slug = payload["params"]["slug"]

        table = get_table()
        store = table.get_item(Key={
            "pk": f"STORE#{store_slug}",
            "sk": f"STORE#{store_slug}",
        })

        if not store.get("Item"):
            return {"status_code": 410, "body": None}

        return {"status_code": 200, "body": {"store": store["Item"]}}
