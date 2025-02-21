from application.schemas.reset_password_schema import ResetPasswordSchema
from common.decorators import load_schema
from models.authentication import reset_password


class ResetPasswordController:
    @staticmethod
    @load_schema(ResetPasswordSchema)
    def process(payload: dict) -> dict:
        body = payload["body"]

        auth_data = {
            "email": body["email"],
            "password": body["password"],
            "confirmation_code": body["confirmation_code"],
        }

        reset_password(auth_data)

        return {"status_code": 204}
