import json

from marshmallow import Schema, pre_load, EXCLUDE
from marshmallow.fields import Nested, Str


class FetchStoresClaims(Schema):
    sub = Str(required=True)

    class Meta:
        unknown = EXCLUDE


class FetchStoresAuthorizerJwt(Schema):
    claims = Nested(FetchStoresClaims, required=True)

    class Meta:
        unknown = EXCLUDE


class FetchStoresAuthorizer(Schema):
    jwt = Nested(FetchStoresAuthorizerJwt, required=True)

    class Meta:
        unknown = EXCLUDE


class HttpRequestContext(Schema):
    method = Str(required=True)

    class Meta:
        unknown = EXCLUDE


class FetchStoresRequestContex(Schema):
    authorizer = Nested(FetchStoresAuthorizer, required=True)
    http = Nested(HttpRequestContext, required=True)

    class Meta:
        unknown = EXCLUDE


class AdminFetchStoresSchema(Schema):
    request_context = Nested(FetchStoresRequestContex, required=True)

    @pre_load
    def input(self, event: dict, **kwargs):
        payload = {}

        if event.get("requestContext"):
            payload["request_context"] = event["requestContext"]

        return payload
