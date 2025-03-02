import json

from marshmallow import Schema, pre_load, EXCLUDE
from marshmallow.fields import Nested, Str


class AdminFetchStoreProductsClaims(Schema):
    sub = Str(required=True)

    class Meta:
        unknown = EXCLUDE


class AdminFetchStoreProductsAuthorizerJwt(Schema):
    claims = Nested(AdminFetchStoreProductsClaims, required=True)

    class Meta:
        unknown = EXCLUDE


class AdminFetchStoreProductsAuthorizer(Schema):
    jwt = Nested(AdminFetchStoreProductsAuthorizerJwt, required=True)

    class Meta:
        unknown = EXCLUDE


class HttpRequestContext(Schema):
    method = Str(required=True)

    class Meta:
        unknown = EXCLUDE


class AdminFetchStoreProductsRequestContex(Schema):
    authorizer = Nested(AdminFetchStoreProductsAuthorizer, required=True)
    http = Nested(HttpRequestContext, required=True)

    class Meta:
        unknown = EXCLUDE


class AdminFetchStoreProductsParams(Schema):
    slug = Str(required=True)


class AdminFetchStoreProductsSchema(Schema):
    params = Nested(AdminFetchStoreProductsParams, required=True)
    request_context = Nested(AdminFetchStoreProductsRequestContex, required=True)

    @pre_load
    def input(self, event: dict, **kwargs):
        payload = {}

        if event.get("pathParameters"):
            payload["params"] = event["pathParameters"]

        if event.get("queryStringParams"):
            payload["query"] = event["queryStringParams"]

        if event.get("body"):
            payload["body"] = json.loads(event["body"])

        if event.get("requestContext"):
            payload["request_context"] = event["requestContext"]

        return payload
