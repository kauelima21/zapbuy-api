from application.schemas.authentication.profile_schema import ProfileSchema
from common.decorators import load_schema
from models.user import find_user_by_id


class ProfileController:
    @staticmethod
    @load_schema(ProfileSchema)
    def process(payload):
        user_id = payload["request_context"]["authorizer"]["jwt"]["claims"]["sub"]

        user = find_user_by_id(user_id)

        if not user:
            return {"status_code": 410, "body": None}

        return {
            "status_code": 200,
            "body": {
                "user": {
                    "user_id": user["user_id"],
                    "email": user["email"],
                    "given_name": user["given_name"],
                    "family_name": user["family_name"],
                }
            }
        }
