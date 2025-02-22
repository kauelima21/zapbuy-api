import json

import pytest
from moto import mock_aws

from handlers.http.authentication import handler
from infra.scripts.create_table import create_table
from models.user import save_user
from ..orchestrator import create_mock_cognito_user


@mock_aws
def test_it_should_return_an_user_profile():
    create_table()

    auth_data = {
        "email": "john.doe@email.com",
        "password": "Ilovecoding@123",
    }

    created_user_id = create_mock_cognito_user(
        user_data=auth_data,
        auto_confirm=False
    )["UserSub"]

    save_user({
        "user_id": created_user_id,
        "email": auth_data["email"],
        "given_name": "John",
        "family_name": "Doe"
    })

    event = {
        "rawPath": "/auth/profile",
        "requestContext": {
            "http": {
                "method": "GET"
            },
            "authorizer": {
                "jwt": {
                    "claims": {
                        "sub": created_user_id
                    }
                }
            }
        }
    }

    response = handler(event, None)
    response_body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert response_body["user"]
    assert response_body["user"]["user_id"] == created_user_id


if __name__ == "__main__":
    pytest.main()
