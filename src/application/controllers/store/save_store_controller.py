from application.schemas.save_store_schema import SaveStoreSchema
from common.database import get_table
from common.decorators import load_schema
from common.utils import generate_slug


class SaveStoreController:
    @staticmethod
    @load_schema(SaveStoreSchema)
    def process(payload: dict) -> dict:
        store_payload = payload["body"]
        store_slug = generate_slug(store_payload["store_name"])

        # TODO: verificar se ja existe loja com a slug

        store_payload["store_slug"] = store_slug
        store_payload["pk"] = f"STORE#{store_slug}"
        store_payload["sk"] = f"STORE#{store_slug}"

        table = get_table()
        table.put_item(Item=store_payload)

        return {"status_code": 201, "body": None}
