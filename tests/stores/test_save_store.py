import json

import pytest
from moto import mock_aws

from handlers.http.store import handler
from infra.scripts.create_table import create_table


@mock_aws
def test_it_should_save_a_store():
    create_table()

    event = {
        "body": json.dumps({
            "store_name": "Minha Loja",
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
        "httpMethod": "POST",
        "path": "/admin/stores"
    }

    response = handler(event, None)
    response_code = response["statusCode"]

    assert response_code == 201


if __name__ == "__main__":
    pytest.main()
