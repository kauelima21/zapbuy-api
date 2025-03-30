from application.schemas.authentication.profile_update_schema import ProfileUpdateSchema
from common.decorators import load_schema
from models.user import find_user_by_id, update_user


class ProfileUpdateController:
    @staticmethod
    @load_schema(ProfileUpdateSchema)
    def process(payload):
        user_id = payload["request_context"]["authorizer"]["jwt"]["claims"]["sub"]

        user = find_user_by_id(user_id)

        if not user:
            return {"status_code": 410, "body": None}

        user["given_name"] = payload["body"]["given_name"]
        user["family_name"] = payload["body"]["family_name"]

        update_user(user)

        return {
            "status_code": 200,
            "body": {"message": "Perfil atualizado com sucesso."},
        }
