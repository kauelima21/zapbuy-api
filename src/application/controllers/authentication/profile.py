from application.schemas.find_user_schema import FindUserSchema
from common.decorators import load_schema
from models.user import find_user_by_id


class FindUser:
    @staticmethod
    @load_schema(FindUserSchema)
    def process(payload):
        user_id = payload["params"]["user_id"]

        user = find_user_by_id(user_id)

        if not user:
            return {"status_code": 410, "body": None}

        return {"status_code": 200, "body": {"user": user}}
