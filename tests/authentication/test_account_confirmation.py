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
    }

    create_mock_cognito_user(user_data={
        "email": "john.doe@email.com",
        "password": "Ilovecoding@123",
    }, auto_confirm=False)

    response = handler(event, None)

    assert response["statusCode"] == 204


if __name__ == "__main__":
    pytest.main()
