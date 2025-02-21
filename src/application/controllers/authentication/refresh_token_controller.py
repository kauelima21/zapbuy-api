from application.schemas.refresh_token_schema import RefreshTokenSchema
from common.decorators import load_schema
from models.authentication import refresh_user_token


class RefreshTokenController:
    @staticmethod
    @load_schema(RefreshTokenSchema)
    def process(payload: dict) -> dict:
        body = payload["body"]
        user_token = body["user_token"]

        refresh_user_token(user_token)

        return {"status_code": 204}
