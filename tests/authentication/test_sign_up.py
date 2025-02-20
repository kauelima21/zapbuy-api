import json

import pytest
from moto import mock_aws

from handlers.http.authentication import handler
from infra.scripts.create_table import create_table
from orchestrator import create_mock_cognito_client_pool


@mock_aws
def test_it_should_sing_up_a_new_user():
    create_table()

    event = {
        "body": json.dumps({
            "email": "john.doe@email.com",
            "password": "Ilovecoding@123",
            "password_confirm": "Ilovecoding@123",
            "first_name": "John",
            "last_name": "Doe",
        }),
        "httpMethod": "POST",
        "path": "/auth/sign-up",
    }

    create_mock_cognito_client_pool()

    response = handler(event, None)
    response_body = json.loads(response["body"])

    assert response_body.get("user_id")
    assert response["statusCode"] == 201


@mock_aws
def test_it_should_not_sing_up_a_new_user_with_different_passwords():
    create_table()

    event = {
        "body": json.dumps({
            "email": "john.doe@email.com",
            "password": "Ilovecoding@123",
            "password_confirm": "Ilikecoding@456",
            "first_name": "John",
            "last_name": "Doe",
        }),
        "httpMethod": "POST",
        "path": "/auth/sign-up",
    }

    create_mock_cognito_client_pool()

    response = handler(event, None)
    response_body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert response_body.get("name") == "ValidationError"


if __name__ == "__main__":
    pytest.main()
