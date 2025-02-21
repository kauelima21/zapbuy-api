from application.schemas.account_confirmation_schema import \
    AccountConfirmationSchema
from common.decorators import load_schema
from models.authentication import confirm_user


class AccountConfirmationController:
    @staticmethod
    @load_schema(AccountConfirmationSchema)
    def process(payload: dict) -> dict:
        body = payload["body"]

        confirm_user(body["email"], body["confirmation_code"])

        return {"status_code": 204}
