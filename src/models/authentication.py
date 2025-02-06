import os

import boto3


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
