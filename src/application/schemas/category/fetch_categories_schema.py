from marshmallow import Schema, pre_load
from marshmallow.fields import Nested, Str


class FetchCategoriesParams(Schema):
    slug = Str(required=True)


class FetchCategoriesSchema(Schema):
    params = Nested(FetchCategoriesParams, required=True)

    @pre_load
    def input(self, event: dict, **kwargs):
        payload = {}

        if event.get("pathParameters"):
            payload["params"] = event["pathParameters"]

        return payload
