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
                    "whatsapp_number": fake.phone_number(),
                    "pk": f"STORE#{slug}", "sk": f"STORE#{slug}",
                    "status": "active" if i not in [4, 8, 10] else "inactive"}
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
        "httpMethod": "GET",
        "path": "/stores/{slug}"
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
        "httpMethod": "GET",
        "path": "/stores/{slug}"
    }

    response = handler(event, None)
    response_code = response["statusCode"]

    assert response_code == 410


if __name__ == "__main__":
    pytest.main()
