from application.schemas.authentication.generate_confirmation_code_schema import GenerateConfirmationCodeSchema
from common.decorators import load_schema
from common.errors import ValidationError
from models.authentication import generate_new_code


class GenerateConfirmationCodeController:
    @staticmethod
    @load_schema(GenerateConfirmationCodeSchema)
    def process(payload: dict) -> dict | None:
        try:
            body = payload["body"]

            generate_new_code(body["email"])

            return {"status_code": 204}
        except Exception as error:
            if str(error) == "UserNotFoundException":
                raise ValidationError("O usuário não está cadastrado.")

            if str(error) == "NotAuthorizedException":
                raise ValidationError("O usuário já está confirmado.")

            raise error
