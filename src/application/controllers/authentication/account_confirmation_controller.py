from application.schemas.authentication.account_confirmation_schema import \
    AccountConfirmationSchema
from common.decorators import load_schema
from common.errors import ValidationError
from models.authentication import confirm_user


class AccountConfirmationController:
    @staticmethod
    @load_schema(AccountConfirmationSchema)
    def process(payload: dict) -> dict | None:
        try:
            body = payload["body"]

            confirm_user(body["email"], body["confirmation_code"])

            return {"status_code": 204}
        except Exception as error:
            if str(error) == "UserNotFoundException":
                raise ValidationError("O usuário não está cadastrado.")
            if str(error) == "NotAuthorizedException":
                raise ValidationError("O usuário já está confirmado.")
            if str(error) == "CodeMismatchException":
                raise ValidationError("Código incorreto ou limite de tentativas atingido. Peça um novo código.")
