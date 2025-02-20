from application.schemas.sign_up_schema import SignUpSchema
from common.decorators import load_schema
from common.errors import ValidationError
from models.authentication import sign_up_user
from models.user import save_user


class SignUpController:
    @staticmethod
    @load_schema(SignUpSchema)
    def process(payload: dict) -> dict:
        body = payload["body"]
        auth_data = {
            "email": body["email"],
            "password": body["password"],
        }
        user_attributes = {
            "email": body["email"],
            "first_name": body["first_name"],
            "last_name": body["last_name"],
        }

        if body["password"] != body["password_confirm"]:
            raise ValidationError("As senhas não conferem")

        user_id = sign_up_user(auth_data, user_attributes)["UserSub"]

        save_user({**user_attributes, "user_id": user_id})

        return {"status_code": 201, "body": {"user_id": user_id}}
