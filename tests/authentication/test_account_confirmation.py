import json

import pytest
from moto import mock_aws

from handlers.http.authentication import handler
from infra.scripts.create_table import create_table
from ..orchestrator import create_mock_cognito_user


@mock_aws
def test_it_should_confirm_an_user_account():
    create_table()

    event = {
        "body": json.dumps({
            "email": "john.doe@email.com",
            "confirmation_code": "123456",
        }),
        "requestContext": {
            "http": {
                "method": "POST",
            }
        },
        "rawPath": "/auth/account-confirmation",
        "routeKey": "POST /auth/account-confirmation"
    }

    create_mock_cognito_user(user_data={
        "email": "john.doe@email.com",
        "password": "Ilovecoding@123",
    }, auto_confirm=False)

    response = handler(event, None)

    assert response["statusCode"] == 204


@mock_aws
def test_it_should_not_confirm_an_user_that_is_not_registered():
    create_table()

    event = {
        "body": json.dumps({
            "email": "joanne.doe@coding.com",
            "confirmation_code": "123456",
        }),
        "requestContext": {
            "http": {
                "method": "POST",
            }
        },
        "rawPath": "/auth/account-confirmation",
        "routeKey": "POST /auth/account-confirmation"
    }

    create_mock_cognito_user(user_data={
        "email": "john.doe@email.com",
        "password": "Ilovecoding@123",
    }, auto_confirm=True)

    response = handler(event, None)
    response_body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert response_body["name"] == "ValidationError"


@mock_aws
@pytest.mark.skip("not implemented")
def test_it_should_generate_a_new_confirm_code():
    create_table()

    event = {
        "body": json.dumps({
            "email": "john.doe@email.com",
        }),
        "requestContext": {
            "http": {
                "method": "POST",
            }
        },
        "rawPath": "/auth/generate-confirmation-code",
        "routeKey": "POST /auth/generate-confirmation-code"
    }

    create_mock_cognito_user(user_data={
        "email": "john.doe@email.com",
        "password": "Ilovecoding@123",
    }, auto_confirm=False)

    response = handler(event, None)

    assert response["statusCode"] == 204


if __name__ == "__main__":
    pytest.main()
