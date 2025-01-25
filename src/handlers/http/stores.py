from application.controllers.fetch_store_products import process
from common.decorators import response_json


@response_json
def handler(event, _):
    products = process(event)

    return {"status_code": 200, "body": {"products": products}}
