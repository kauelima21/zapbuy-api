import json

from marshmallow import Schema, pre_load
from marshmallow.fields import Nested, Str


class FetchStoreProductsParams(Schema):
    store_slug = Str(required=True, description="store slug")


class FetchStoreProductsSchema(Schema):
    params = Nested(FetchStoreProductsParams, required=True)

    @pre_load
    def input(self, event: dict, **kwargs):
        payload = {}

        if event.get("pathParameters"):
            payload["params"] = event["pathParameters"]

        if event.get("queryStringParams"):
            payload["query"] = event["queryStringParams"]

        if event.get("body"):
            payload["body"] = json.loads(event["body"])

        return payload
