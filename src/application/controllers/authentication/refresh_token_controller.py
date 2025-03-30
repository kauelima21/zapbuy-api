from botocore.exceptions import ClientError

from application.schemas.authentication.refresh_token_schema import RefreshTokenSchema
from common.decorators import load_schema
from common.errors import UnauthorizedError
from models.authentication import refresh_user_token


class RefreshTokenController:
    @staticmethod
    @load_schema(RefreshTokenSchema)
    def process(payload: dict) -> dict:
        body = payload["body"]
        user_token = body["user_token"]

        try:
            response = refresh_user_token(user_token)["AuthenticationResult"]

            return {"status_code": 201, "body": {"access_token": response["AccessToken"]}}
        except ClientError:
            error_message = "Credenciais inválidas."
            raise UnauthorizedError(error_message)
