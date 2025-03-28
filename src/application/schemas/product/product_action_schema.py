import json

from marshmallow import Schema, pre_load, EXCLUDE
from marshmallow.fields import Nested, Str, Integer, List


class ProfileClaims(Schema):
    sub = Str(required=True)

    class Meta:
        unknown = EXCLUDE


class ProfileAuthorizerJwt(Schema):
    claims = Nested(ProfileClaims, required=True)

    class Meta:
        unknown = EXCLUDE


class ProfileAuthorizer(Schema):
    jwt = Nested(ProfileAuthorizerJwt, required=True)

    class Meta:
        unknown = EXCLUDE


class HttpRequestContext(Schema):
    method = Str(required=True)

    class Meta:
        unknown = EXCLUDE


class ProfileRequestContex(Schema):
    authorizer = Nested(ProfileAuthorizer, required=True)
    http = Nested(HttpRequestContext, required=True)

    class Meta:
        unknown = EXCLUDE


class ProductCategory(Schema):
    name = Str(required=True)
    value = Str(required=True)


class ProductActionParams(Schema):
    slug = Str(required=True)
    product_id = Str(required=True)


class ProductActionBody(Schema):
    file_name = Str(required=True)
    file_type = Str(required=True)


class ProductActionSchema(Schema):
    body = Nested(ProductActionBody, required=True)
    params = Nested(ProductActionParams, required=True)
    request_context = Nested(ProfileRequestContex, required=True)

    @pre_load
    def input(self, event: dict, **kwargs):
        payload = {}

        if event.get("pathParameters"):
            payload["params"] = event["pathParameters"]

        if event.get("body"):
            payload["body"] = json.loads(event["body"])

        if event.get("requestContext"):
            payload["request_context"] = event["requestContext"]

        return payload
