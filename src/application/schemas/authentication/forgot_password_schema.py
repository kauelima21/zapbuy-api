import json

from marshmallow import Schema, pre_load
from marshmallow.fields import Nested, Str


class ForgotPasswordBody(Schema):
    email = Str(required=True)


class ForgotPasswordSchema(Schema):
    body = Nested(ForgotPasswordBody, required=True)

    @pre_load
    def input(self, event: dict, **kwargs):
        payload = {}

        if event.get("body"):
            payload["body"] = json.loads(event["body"])

        return payload
