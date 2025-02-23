import os

import boto3
from botocore.exceptions import ClientError

from common.errors import UnauthorizedError


def get_new_client():
    return boto3.client("cognito-idp")


def sign_up_user(auth_data: dict, user_attributes: dict) -> dict:
    client = get_new_client()
    parsed_user_attributes = [
        {"Name": key, "Value": value} for key, value in user_attributes.items()
    ]

    return client.sign_up(
        ClientId=os.environ.get("COGNITO_CLIENT_ID"),
        Username=auth_data["email"],
        Password=auth_data["password"],
        UserAttributes=parsed_user_attributes,
    )


def sign_in_user(auth_data: dict) -> dict | None:
    try:
        client = get_new_client()

        initiate_auth_params = {
            "ClientId": os.environ.get("COGNITO_CLIENT_ID"),
            "AuthFlow": "USER_PASSWORD_AUTH",
            "AuthParameters": {
                "USERNAME": auth_data["email"],
                "PASSWORD": auth_data["password"]
            }
        }

        return client.initiate_auth(**initiate_auth_params)
    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        error_message = "Credenciais inválidas."

        if error_code == "UserNotConfirmedException":
            error_message = "Você precisa confirmar sua conta antes de realizar o login."

        raise UnauthorizedError(error_message)


def refresh_user_token(user_token: str) -> dict:
    client = get_new_client()

    initiate_auth_params = {
        "ClientId": os.environ.get("COGNITO_CLIENT_ID"),
        "AuthFlow": "REFRESH_TOKEN",
        "AuthParameters": {
            "REFRESH_TOKEN": user_token
        }
    }

    return client.initiate_auth(**initiate_auth_params)


def confirm_user(user_name: dict, confirmation_code: str):
    client = get_new_client()

    client.confirm_sign_up(
        ClientId=os.environ.get("COGNITO_CLIENT_ID"),
        Username=user_name,
        ConfirmationCode=confirmation_code
    )


def forgot_password(user_name: str) -> dict:
    client = get_new_client()

    return client.forgot_password(
        ClientId=os.environ.get("COGNITO_CLIENT_ID"),
        Username=user_name,
    )


def reset_password(auth_data: dict):
    client = get_new_client()

    client.confirm_forgot_password(
        ClientId=os.environ.get("COGNITO_CLIENT_ID"),
        Username=auth_data["email"],
        Password=auth_data["password"],
        ConfirmationCode=auth_data["confirmation_code"],
    )
