import json

import pytest
from faker.proxy import Faker
from moto import mock_aws

from common.database import get_table
from handlers.http.user import handler
from infra.scripts.create_table import create_table


def populate_users(user_id: str):
    with get_table().batch_writer() as batch:
        fake = Faker(locale="pt_BR")
        for i in range(15):
            if i != 1:
                id_user = fake.uuid4()
            else:
                id_user = user_id
            item = {"first_name": fake.first_name(), "last_name": fake.last_name(),
                    "whatsapp_number": fake.phone_number(), "email": fake.email(),
                    "pk": f"USER#{id_user}", "sk": f"USER#{id_user}",
                    "status": "active" if i not in [4, 8, 10] else "inactive"}
            batch.put_item(Item=item)


@mock_aws
def test_it_should_find_a_user():
    create_table()
    user_id = "id-user"

    populate_users(user_id)

    event = {
        "pathParameters": {
            "user_id": user_id,
        },
        "httpMethod": "GET",
        "path": "/users/{user_id}"
    }

    response = handler(event, None)
    response_body = json.loads(response["body"])
    response_code = response["statusCode"]

    assert response_body
    assert response_code == 200


@mock_aws
def test_it_should_not_find_a_user():
    create_table()
    user_id = "id-user"

    populate_users(user_id)

    event = {
        "pathParameters": {
            "user_id": "random-slug-fake",
        },
        "httpMethod": "GET",
        "path": "/users/{user_id}"
    }

    response = handler(event, None)
    response_code = response["statusCode"]

    assert response_code == 410


if __name__ == "__main__":
    pytest.main()
