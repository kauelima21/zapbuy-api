import json

import pytest
from faker.proxy import Faker
from moto import mock_aws

from common.database import get_table
from handlers.http.stores import handler
from infra.scripts.create_table import create_table


@mock_aws
def test_it_should_fetch_store_products():
    create_table()
    store_slug = "minha-loja"

    with get_table().batch_writer() as batch:
        fake = Faker(locale="en_PH")
        for i in range(15):
            item = {"product_name": fake.random_company_product(),
                    "price": fake.pricetag(), "pk": f"PRODUCT#{fake.uuid4()}"}
            if i % 2 == 0:
                item["sk"] = f"STORE#{store_slug}"
            else:
                item["sk"] = f"STORE#{fake.slug()}"
            batch.put_item(Item=item)

    event = {
        "pathParameters": {
            "store_slug": store_slug
        }
    }

    response = handler(event, None)
    response_body = json.loads(response["body"])

    assert len(response_body["products"]) > 0


@mock_aws
def test_it_should_not_fetch_store_products():
    create_table()
    event = {
        "pathParameters": "minha-loja"
    }

    response = handler(event, None)
    response_body = json.loads(response["body"])

    assert len(response_body["products"]) == 0


if __name__ == "__main__":
    pytest.main()
