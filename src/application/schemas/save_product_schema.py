import json

from marshmallow import Schema, pre_load
from marshmallow.fields import Nested, Str, Integer, List


class ProfileClaims(Schema):
    sub = Str(required=True)


class ProfileAuthorizer(Schema):
    claims = Nested(ProfileClaims, required=True)


class ProfileRequestContex(Schema):
    authorizer = Nested(ProfileAuthorizer, required=True)


class ProductCategory(Schema):
    name = Str(required=True)
    value = Str(required=True)


class SaveProductParams(Schema):
    slug = Str(required=True)


class SaveProductBody(Schema):
    name = Str(required=True)
    description = Str(required=True)
    price_in_cents = Integer(required=True)
    categories = List(Nested(ProductCategory), required=False)


class SaveProductSchema(Schema):
    body = Nested(SaveProductBody, required=True)
    params = Nested(SaveProductParams, required=True)
    request_context = Nested(ProfileRequestContex, required=True)

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
