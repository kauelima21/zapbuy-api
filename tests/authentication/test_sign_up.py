import json

import pytest
from moto import mock_aws

from handlers.http.authentication import handler
from infra.scripts.create_table import create_table
from ..orchestrator import create_mock_cognito_client_pool, create_mock_cognito_user


@mock_aws
def test_it_should_sing_up_a_new_user():
    create_table()

    event = {
        "body": json.dumps({
            "email": "john.doe@email.com",
            "password": "Ilovecoding@123",
            "password_confirm": "Ilovecoding@123",
            "given_name": "John",
            "family_name": "Doe",
        }),
        "requestContext": {
            "http": {
                "method": "POST",
            }
        },
        "rawPath": "/auth/sign-up",
        "routeKey": "POST /auth/sign-up"
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
            "given_name": "John",
            "family_name": "Doe",
        }),
        "requestContext": {
            "http": {
                "method": "POST",
            }
        },
        "rawPath": "/auth/sign-up",
        "routeKey": "POST /auth/sign-up"
    }

    create_mock_cognito_client_pool()

    response = handler(event, None)
    response_body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert response_body.get("name") == "ValidationError"


@mock_aws
def test_it_should_not_sing_up_a_new_user_with_email_already_saved():
    create_table()

    user_payload = {
        "email": "joanne.doe@email.com",
        "password": "Ilikecoding@123",
    }
    create_mock_cognito_user(user_payload)

    event = {
        "body": json.dumps({
            "email": "joanne.doe@email.com",
            "password": "Ilovecoding@123",
            "password_confirm": "Ilovecoding@123",
            "given_name": "John",
            "family_name": "Doe",
        }),
        "requestContext": {
            "http": {
                "method": "POST",
            }
        },
        "rawPath": "/auth/sign-up",
        "routeKey": "POST /auth/sign-up"
    }

    response = handler(event, None)
    response_body = json.loads(response["body"])

    assert response["statusCode"] == 409
    assert response_body.get("name") == "ConflictError"


@mock_aws
def test_it_should_not_sing_up_a_new_user_with_a_password_that_doesnt_fit():
    create_table()

    event = {
        "body": json.dumps({
            "email": "joanne.doe@email.com",
            "password": "senhapilantra",
            "password_confirm": "senhapilantra",
            "given_name": "Joanne",
            "family_name": "Doe"
        }),
        "requestContext": {
            "http": {
                "method": "POST",
            }
        },
        "rawPath": "/auth/sign-up",
        "routeKey": "POST /auth/sign-up"
    }

    create_mock_cognito_client_pool()

    response = handler(event, None)
    response_body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert response_body.get("name") == "ValidationError"


if __name__ == "__main__":
    pytest.main()
