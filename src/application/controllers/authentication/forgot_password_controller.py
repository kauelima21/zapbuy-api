from application.schemas.authentication.forgot_password_schema import ForgotPasswordSchema
from common.decorators import load_schema
from models.authentication import forgot_password


class ForgotPasswordController:
    @staticmethod
    @load_schema(ForgotPasswordSchema)
    def process(payload: dict) -> dict:
        body = payload["body"]

        forgot_password(body["email"])

        return {"status_code": 204}
