import json

from marshmallow import Schema, pre_load
from marshmallow.fields import Nested, Str


class SignInBody(Schema):
    email = Str(required=True)
    password = Str(required=True)


class SignInSchema(Schema):
    body = Nested(SignInBody, required=True)

    @pre_load
    def input(self, event: dict, **kwargs):
        payload = {}

        if event.get("body"):
            payload["body"] = json.loads(event["body"])

        return payload
