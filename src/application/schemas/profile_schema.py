import json

from marshmallow import Schema, pre_load
from marshmallow.fields import Nested, Str


class ProfileClaims(Schema):
    sub = Str(required=True, description="user id")


class ProfileAuthorizer(Schema):
    claims = Nested(ProfileClaims, required=True)


class ProfileRequestContex(Schema):
    authorizer = Nested(ProfileAuthorizer, required=True)


class ProfileSchema(Schema):
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
