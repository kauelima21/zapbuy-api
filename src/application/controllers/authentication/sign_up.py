from application.schemas.sign_up_schema import SignUpSchema
from common.decorators import load_schema
from models.authentication import sign_up_user
from models.user import save_user


class SignUpController:
    @staticmethod
    @load_schema(SignUpSchema)
    def process(payload: dict) -> dict:
        body = payload["body"]
        auth_data = {
            "email": body["email"],
            "password": body["password"],
        }
        restrict_keys = ["password", "password_confirm"]
        user_attributes = {
            key: value
            for key, value in body.items()
            if key not in restrict_keys
        }

        # tratar o caso password_confirm

        user_id = sign_up_user(auth_data, user_attributes)["UserSub"]

        save_user(
            {
                "user_id": user_id,
                "email": body["email"],
                "first_name": body["first_name"],
                "last_name": body["last_name"],
            }
        )

        return {"status_code": 201, "body": {"user_id": user_id}}
