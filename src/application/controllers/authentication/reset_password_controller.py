from application.schemas.authentication.reset_password_schema import ResetPasswordSchema
from common.decorators import load_schema
from common.errors import ValidationError
from models.authentication import reset_password


class ResetPasswordController:
    @staticmethod
    @load_schema(ResetPasswordSchema)
    def process(payload: dict) -> dict | None:
        try:
            body = payload["body"]

            auth_data = {
                "email": body["email"],
                "password": body["password"],
                "confirmation_code": body["confirmation_code"],
            }

            reset_password(auth_data)

            return {"status_code": 204}
        except Exception as error:
            if str(error) == "UserNotFoundException":
                raise ValidationError("O usuário informado não existe.")
            if str(error) == "InvalidPasswordException":
                raise ValidationError("A senha não segue as regras de validação.")
