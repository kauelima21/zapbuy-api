import json

import pytest
from moto import mock_aws

from handlers.http.products import handler
from infra.scripts.create_table import create_table
from models.store import save_store


@pytest.fixture()
def get_event():
    def create_event(store_slug, owner_id):
        return {
            "pathParameters": {
                "slug": store_slug,
            },
            "body": json.dumps({
                "name": "sapato",
                "description": "sapato bonito",
                "price_in_cents": 1000,
                "category": "sapatos",
                "s3_object_image": f"{store_slug}/produto-bonito.jpg",
            }),
            "rawPath": "/admin/stores/{slug}/products",
            "requestContext": {
                "http": {
                    "method": "POST"
                },
                "authorizer": {
                    "jwt": {
                        "claims": {
                            "sub": owner_id
                        }
                    }
                }
            },
            "routeKey": "POST /admin/stores/{slug}/products"
        }

    return create_event


@mock_aws
def test_it_should_save_a_product(get_event):
    create_table()
    store_slug = "minha-loja"
    owner_id = "user-id"

    save_store({
        "owner_id": owner_id,
        "store_slug": store_slug
    })

    event = get_event(store_slug, owner_id)

    response = handler(event, None)
    response_body = json.loads(response["body"])
    response_code = response["statusCode"]

    assert response_body
    assert response_code == 201


@mock_aws
def test_it_should_not_save_a_product_with_invalid_store(get_event):
    create_table()
    store_slug = "minha-loja"
    owner_id = "user-id"

    event = get_event(store_slug, owner_id)

    response = handler(event, None)
    response_body = json.loads(response["body"])
    response_code = response["statusCode"]

    assert response_body["name"] == "ValidationError"
    assert response_code == 400


@mock_aws
def test_it_should_not_save_a_product_with_invalid_user(get_event):
    create_table()
    store_slug = "minha-loja"
    owner_id = "user-id"

    save_store({
        "owner_id": owner_id,
        "store_slug": store_slug
    })

    event = get_event(store_slug, "outro-user-id")

    response = handler(event, None)
    response_body = json.loads(response["body"])
    response_code = response["statusCode"]

    assert response_body["name"] == "ForbiddenError"
    assert response_code == 403


if __name__ == "__main__":
    pytest.main()
