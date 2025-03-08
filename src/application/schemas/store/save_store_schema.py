import json

from marshmallow import Schema, pre_load, EXCLUDE
from marshmallow.fields import Nested, Str, List


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


class WorkDays(Schema):
    start_day = Str(required=True)
    last_day = Str(required=True)


class WorkHours(Schema):
    start_hour = Str(required=True)
    last_hour = Str(required=True)


class Variants(Schema):
    variant_name = Str(required=True)
    values = List(Str, required=True)


class SaveStoreBody(Schema):
    store_name = Str(required=True)
    whatsapp_number = Str(required=True)
    work_days = Nested(WorkDays, required=True)
    work_hours = Nested(WorkHours, required=True)
    variants = List(Nested(Variants, required=False))


class SaveStoreSchema(Schema):
    body = Nested(SaveStoreBody, required=True)
    request_context = Nested(ProfileRequestContex, required=True)

    @pre_load
    def input(self, event: dict, **kwargs):
        payload = {}

        if event.get("body"):
            payload["body"] = json.loads(event["body"])

        if event.get("requestContext"):
            payload["request_context"] = event["requestContext"]

        return payload
