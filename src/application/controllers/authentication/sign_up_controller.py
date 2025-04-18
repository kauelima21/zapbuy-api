from application.schemas.authentication.sign_up_schema import SignUpSchema
from common.decorators import load_schema
from common.errors import ValidationError, ConflictError
from models.authentication import sign_up_user
from models.user import save_user, find_user_by_email


class SignUpController:
    @staticmethod
    @load_schema(SignUpSchema)
    def process(payload: dict) -> dict | None:
        body = payload["body"]
        auth_data = {
            "email": body["email"],
            "password": body["password"],
        }
        user_attributes = {
            "email": body["email"],
            "given_name": body["given_name"],
            "family_name": body["family_name"],
        }

        if body["password"] != body["password_confirm"]:
            raise ValidationError("As senhas informadas não conferem.")

        try:
            user_id = sign_up_user(auth_data, user_attributes)["UserSub"]

            save_user({**user_attributes, "user_id": user_id})

            return {"status_code": 201, "body": {"user_id": user_id}}
        except Exception as error:
            if str(error) == "UsernameExistsException":
                raise ConflictError("O e-mail informado já está em uso.")

            if str(error) == "InvalidPasswordException":
                raise ValidationError("A senha não segue as regras de validação.")

            raise error
