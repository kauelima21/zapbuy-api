import json

import pytest
from moto import mock_aws

from handlers.http.authentication import handler
from infra.scripts.create_table import create_table
from models.authentication import sign_in_user
from ..orchestrator import create_mock_cognito_user


@mock_aws
def test_it_should_refresh_token():
    create_table()

    auth_data = {
        "email": "john.doe@email.com",
        "password": "Ilovecoding@123",
    }

    create_mock_cognito_user(user_data=auth_data, auto_confirm=True)

    sign_data = sign_in_user(auth_data)["AuthenticationResult"]

    event = {
        "body": json.dumps({
            "user_token": sign_data["RefreshToken"],
        }),
        "requestContext": {
            "http": {
                "method": "POST",
            }
        },
        "rawPath": "/auth/refresh-token",
        "routeKey": "POST /auth/refresh-token"
    }

    response = handler(event, None)
    response_body = json.loads(response["body"])

    assert response["statusCode"] == 201
    assert response_body["access_token"]


if __name__ == "__main__":
    pytest.main()
