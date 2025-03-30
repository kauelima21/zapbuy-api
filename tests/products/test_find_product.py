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
                    "product_id": product_id, "description": "", "s3_object_image": "",
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
def test_it_should_find_a_product():
    create_table()
    store_slug = "minha-loja"
    product_id = "id-produto"

    populate_products(store_slug)

    fake = Faker(locale="en_PH")
    item = {"name": fake.random_company_product(), "status": "active", "categories": "{}",
            "price_in_cents": 25000, "sk": f"PRODUCT#{product_id}", "product_id": product_id,
            "pk": f"STORE#{store_slug}", "description": "", "s3_object_image": "", "store_slug": store_slug}
    get_table().put_item(Item=item)

    event = {
        "pathParameters": {
            "slug": store_slug,
            "product_id": product_id
        },
        "requestContext": {
            "http": {
                "method": "GET",
            }
        },
        "rawPath": "/stores/{slug}/products/{product_id}",
        "routeKey": "GET /stores/{slug}/products/{product_id}"
    }

    response = handler(event, None)
    response_body = json.loads(response["body"])
    response_code = response["statusCode"]

    assert response_body
    assert response_code == 200


@mock_aws
def test_it_should_not_find_a_product():
    create_table()
    event = {
        "pathParameters": {
            "slug": "slug",
            "product_id": "id"
        },
        "requestContext": {
            "http": {
                "method": "GET",
            }
        },
        "rawPath": "/stores/{slug}/products/{product_id}",
        "routeKey": "GET /stores/{slug}/products/{product_id}"
    }

    response = handler(event, None)
    response_code = response["statusCode"]

    assert response_code == 410


if __name__ == "__main__":
    pytest.main()
