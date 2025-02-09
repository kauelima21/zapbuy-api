from application.schemas.profile_schema import ProfileSchema
from common.decorators import load_schema
from models.user import find_user_by_id


class ProfileController:
    @staticmethod
    @load_schema(ProfileSchema)
    def process(payload):
        user_id = payload["request_context"]["authorizer"]["claims"]["sub"]

        user = find_user_by_id(user_id)

        if not user:
            return {"status_code": 410, "body": None}

        return {"status_code": 200, "body": {"user": user}}
