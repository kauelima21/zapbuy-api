import json

import pytest
from faker.proxy import Faker
from moto import mock_aws

from common.database import get_table
from handlers.http.products import handler
from infra.scripts.create_table import create_table


def populate_products(store_slug: str):
    with get_table().batch_writer() as batch:
        fake = Faker(locale="en_PH")
        for i in range(15):
            product_id = fake.uuid4()
            item = {"name": fake.random_company_product(), "categories": "{}",
                    "product_id": product_id, "description": "",
                    "price_in_cents": 1000, "pk": f"PRODUCT#{product_id}"}
            if i % 2 == 0:
                item["sk"] = f"STORE#{store_slug}"
                item["status"] = "active" if i not in [4, 8, 10] else "inactive"
                item["store_slug"] = store_slug
            else:
                item["sk"] = f"STORE#{fake.slug()}"
                item["status"] = "active"
                item["store_slug"] = fake.slug()
            batch.put_item(Item=item)


@mock_aws
def test_it_should_fetch_store_products():
    create_table()
    store_slug = "minha-loja"

    populate_products(store_slug)

    event = {
        "pathParameters": {
            "slug": store_slug
        },
        "requestContext": {
            "http": {
                "method": "GET",
            }
        },
        "rawPath": "/stores/{slug}/products",
        "routeKey": "GET /stores/{slug}/products"
    }

    response = handler(event, None)
    response_body = json.loads(response["body"])

    assert len(response_body["products"]) > 0


@mock_aws
def test_it_should_fetch_admin_store_products():
    create_table()
    store_slug = "minha-loja"

    populate_products(store_slug)

    event = {
        "pathParameters": {
            "slug": store_slug
        },
        "requestContext": {
            "http": {
                "method": "GET",
            }
        },
        "rawPath": "/admin/stores/{slug}/products",
        "routeKey": "GET /stores/{slug}/products"
    }

    response = handler(event, None)
    response_body = json.loads(response["body"])

    assert len(response_body["products"]) > 0


@mock_aws
def test_it_should_not_fetch_store_products():
    create_table()
    event = {
        "pathParameters": {
            "slug": "slug"
        },
        "requestContext": {
            "http": {
                "method": "GET",
            }
        },
        "rawPath": "/stores/{slug}/products",
        "routeKey": "GET /stores/{slug}/products"
    }

    response = handler(event, None)
    response_body = json.loads(response["body"])

    assert len(response_body["products"]) == 0


if __name__ == "__main__":
    pytest.main()
