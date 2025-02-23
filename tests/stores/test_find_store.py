import json

import pytest
from faker.proxy import Faker
from moto import mock_aws

from common.database import get_table
from handlers.http.store import handler
from infra.scripts.create_table import create_table


def populate_stores(store_slug: str):
    with get_table().batch_writer() as batch:
        fake = Faker(locale="pt_BR")
        for i in range(15):
            if i != 1:
                slug = fake.slug()
            else:
                slug = store_slug
            item = {"store_name": Faker(locale="en_PH").random_company_product(),
                    "whatsapp_number": fake.phone_number(), "store_slug": slug,
                    "pk": f"STORE#{slug}", "sk": f"OWNER#{fake.uuid4()}",
                    "status": "active" if i not in [4, 8, 10] else "inactive",
                    "work_days": {}, "work_hours": {}, "owner_id": ""}
            batch.put_item(Item=item)


@mock_aws
def test_it_should_find_a_store():
    create_table()
    store_slug = "minha-loja"

    populate_stores(store_slug)

    event = {
        "pathParameters": {
            "slug": store_slug,
        },
        "requestContext": {
            "http": {
                "method": "GET",
            }
        },
        "rawPath": "/stores/{slug}",
        "routeKey": "GET /stores/{slug}"
    }

    response = handler(event, None)
    response_body = json.loads(response["body"])
    response_code = response["statusCode"]

    assert response_body
    assert response_code == 200


@mock_aws
def test_it_should_not_find_a_store():
    create_table()
    store_slug = "minha-loja"

    populate_stores(store_slug)

    event = {
        "pathParameters": {
            "slug": "random-slug-fake",
        },
        "requestContext": {
            "http": {
                "method": "GET",
            }
        },
        "rawPath": "/stores/{slug}",
        "routeKey": "GET /stores/{slug}"
    }

    response = handler(event, None)
    response_code = response["statusCode"]
    response_body = json.loads(response["body"])

    assert response_code == 404
    assert response_body["name"] == "NotFoundError"


if __name__ == "__main__":
    pytest.main()
