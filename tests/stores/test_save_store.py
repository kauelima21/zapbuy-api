import json

import pytest
from moto import mock_aws

from handlers.http.store import handler
from infra.scripts.create_table import create_table
from models.store import save_store


@mock_aws
def test_it_should_save_a_store():
    create_table()

    event = {
        "body": json.dumps({
            "store_name": "Minha Loja",
            "owner_id": "id-user",
            "whatsapp_number": "99999999999",
            "work_hours": {
                "start_hour": "08:00",
                "last_hour": "18:00",
            },
            "work_days": {
                "start_day": "Segunda-feira",
                "last_day": "Sexta-feira",
            },
        }),
        "requestContext": {
            "http": {
                "method": "POST",
            }
        },
        "rawPath": "/admin/stores"
    }

    response = handler(event, None)
    response_code = response["statusCode"]

    assert response_code == 201


@mock_aws
def test_it_should_not_save_a_store_with_slug_already_saved():
    create_table()

    store_payload = {
        "store_name": "Minha Loja",
        "owner_id": "id-user",
        "whatsapp_number": "99999999999",
        "work_hours": {
            "start_hour": "08:00",
            "last_hour": "18:00",
        },
        "work_days": {
            "start_day": "Segunda-feira",
            "last_day": "Sexta-feira",
        },
    }

    save_store({**store_payload, "store_slug": "minha-loja"})

    event = {
        "body": json.dumps(store_payload),
        "requestContext": {
            "http": {
                "method": "POST",
            }
        },
        "rawPath": "/admin/stores"
    }

    response = handler(event, None)
    response_code = response["statusCode"]
    response_body = json.loads(response["body"])

    assert response_code == 409
    assert response_body.get("name") == "ConflictError"


if __name__ == "__main__":
    pytest.main()
