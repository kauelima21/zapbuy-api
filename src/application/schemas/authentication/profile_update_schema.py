import json

from marshmallow import Schema, pre_load, EXCLUDE
from marshmallow.fields import Nested, Str


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


class ProfileUpdateBody(Schema):
    given_name = Str(required=True)
    family_name = Str(required=True)


class ProfileUpdateSchema(Schema):
    request_context = Nested(ProfileRequestContex, required=True)
    body = Nested(ProfileUpdateBody, required=True)

    @pre_load
    def input(self, event: dict, **kwargs):
        payload = {}

        if event.get("requestContext"):
            payload["request_context"] = event["requestContext"]

        if event.get("body"):
            payload["body"] = json.loads(event["body"])

        return payload
