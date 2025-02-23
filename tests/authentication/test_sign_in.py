import json

import pytest
from moto import mock_aws

from handlers.http.authentication import handler
from infra.scripts.create_table import create_table
from ..orchestrator import create_mock_cognito_user


@mock_aws
def test_it_should_sing_in_an_user():
    create_table()

    event = {
        "body": json.dumps({
            "email": "john.doe@email.com",
            "password": "Ilovecoding@123",
        }),
        "requestContext": {
            "http": {
                "method": "POST",
            }
        },
        "rawPath": "/auth/sign-in",
        "routeKey": "POST /auth/sign-in"
    }

    create_mock_cognito_user(json.loads(event["body"]))

    response = handler(event, None)
    response_body = json.loads(response["body"])

    assert response_body.get("access_token")
    assert response_body.get("refresh_token")
    assert response["statusCode"] == 200


@mock_aws
def test_it_should_not_sing_in_an_user_unconfirmed():
    create_table()

    event = {
        "body": json.dumps({
            "email": "john.doe@email.com",
            "password": "Ilovecoding@123",
        }),
        "requestContext": {
            "http": {
                "method": "POST",
            }
        },
        "rawPath": "/auth/sign-in",
        "routeKey": "POST /auth/sign-in"
    }

    create_mock_cognito_user(json.loads(event["body"]), False)

    response = handler(event, None)
    response_body = json.loads(response["body"])

    assert response_body["name"] == "UnauthorizedError"
    assert response["statusCode"] == 401


if __name__ == "__main__":
    pytest.main()
