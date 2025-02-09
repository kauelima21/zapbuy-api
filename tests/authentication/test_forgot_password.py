import json

import pytest
from moto import mock_aws

from handlers.http.authentication import handler
from infra.scripts.create_table import create_table
from orchestrator import create_mock_cognito_user


@mock_aws
def test_it_should_permit_an_user_forgot_a_password():
    create_table()

    event = {
        "body": json.dumps({
            "email": "john.doe@email.com",
        }),
        "httpMethod": "POST",
        "path": "/auth/forgot-password",
    }

    create_mock_cognito_user(user_data={
        "email": "john.doe@email.com",
        "password": "Ilovecoding@123",
    }, auto_confirm=True)

    response = handler(event, None)

    assert response["statusCode"] == 204


if __name__ == "__main__":
    pytest.main()
