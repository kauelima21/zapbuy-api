from marshmallow import Schema, pre_load
from marshmallow.fields import Nested, Str, Int


class FetchStoreProductsParams(Schema):
    slug = Str(required=True)


class FetchStoreProductsQuery(Schema):
    per_page = Int(required=False)
    last_pk = Str(required=False)
    last_sk = Str(required=False)


class FetchStoreProductsSchema(Schema):
    params = Nested(FetchStoreProductsParams, required=True)
    query = Nested(FetchStoreProductsQuery, required=False)

    @pre_load
    def input(self, event: dict, **kwargs):
        payload = {}

        if event.get("pathParameters"):
            payload["params"] = event["pathParameters"]

        if event.get("queryStringParameters"):
            payload["query"] = event["queryStringParameters"]

        return payload
