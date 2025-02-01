from application.schemas.find_store_schema import FindStoreSchema
from common.decorators import load_schema
from models.store import find_store_by_slug


class FindStore:
    @staticmethod
    @load_schema(FindStoreSchema)
    def process(payload):
        store_slug = payload["params"]["slug"]

        store = find_store_by_slug(store_slug)

        if not store:
            return {"status_code": 410, "body": None}

        return {"status_code": 200, "body": {"store": store}}
