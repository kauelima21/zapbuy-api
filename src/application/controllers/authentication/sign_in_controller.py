from application.schemas.authentication.sign_in_schema import SignInSchema
from common.decorators import load_schema
from models.authentication import sign_in_user


class SignInController:
    @staticmethod
    @load_schema(SignInSchema)
    def process(payload: dict) -> dict:
        body = payload["body"]
        auth_data = {
            "email": body["email"],
            "password": body["password"],
        }

        response = sign_in_user(auth_data)["AuthenticationResult"]

        access_token_info = {
            "access_token": response["AccessToken"],
            "refresh_token": response["RefreshToken"],
            "expires_in": response["ExpiresIn"]
        }

        return {"status_code": 200, "body": access_token_info}
