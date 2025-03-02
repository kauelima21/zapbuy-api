import json

import pytest
from faker.proxy import Faker
from moto import mock_aws

from common.database import get_table
from common.utils import generate_slug
from handlers.http.store import handler
from infra.scripts.create_table import create_table


def populate_stores(owner_id: str):
    with get_table().batch_writer() as batch:
        fake = Faker(locale="pt_BR")
        for i in range(15):
            if i % 2 == 0:
                owner = owner_id
            else:
                owner = fake.uuid4()
            store_name = Faker(locale="en_PH").random_company_product()
            item = {"store_name": store_name, "store_slug": generate_slug(store_name),
                    "whatsapp_number": fake.phone_number(),
                    "pk": f"STORE#{fake.slug()}", "sk": f"OWNER#{owner}",
                    "status": "active" if i not in [4, 8, 10] else "inactive",
                    "work_days": {}, "work_hours": {}, "owner_id": owner}
            batch.put_item(Item=item)


@mock_aws
def test_it_should_fetch_stores():
    create_table()
    owner_id = "id-user"

    populate_stores(owner_id)

    event = {
        "requestContext": {
            "http": {
                "method": "GET",
            },
            "authorizer": {
                "jwt": {
                    "claims": {
                        "sub": owner_id
                    }
                }
            }
        },
        "rawPath": "/admin/stores",
        "routeKey": "GET /admin/stores"
    }

    response = handler(event, None)
    response_body = json.loads(response["body"])
    response_code = response["statusCode"]

    assert len(response_body["stores"]) > 0
    assert response_code == 200


@mock_aws
def test_it_should_not_fetch_stores():
    create_table()
    owner_id = "id-user"

    populate_stores(owner_id)

    event = {
        "requestContext": {
            "http": {
                "method": "GET",
            },
            "authorizer": {
                "jwt": {
                    "claims": {
                        "sub": "other_user"
                    }
                }
            }
        },
        "rawPath": "/admin/stores",
        "routeKey": "GET /admin/stores"
    }

    response = handler(event, None)
    response_body = json.loads(response["body"])
    response_code = response["statusCode"]

    assert response_code == 200
    assert len(response_body["stores"]) == 0


if __name__ == "__main__":
    pytest.main()
