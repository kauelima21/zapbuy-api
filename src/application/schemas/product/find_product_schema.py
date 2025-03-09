import json

from marshmallow import Schema, pre_load
from marshmallow.fields import Nested, Str


class FindProductParams(Schema):
    slug = Str(required=True)
    product_id = Str(required=True)


class FindProductSchema(Schema):
    params = Nested(FindProductParams, required=True)

    @pre_load
    def input(self, event: dict, **kwargs):
        payload = {}

        if event.get("pathParameters"):
            payload["params"] = event["pathParameters"]

        return payload
