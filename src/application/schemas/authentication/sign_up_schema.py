import json

from marshmallow import Schema, pre_load
from marshmallow.fields import Nested, Str


class SignUpBody(Schema):
    email = Str(required=True)
    password = Str(required=True)
    password_confirm = Str(required=True)
    given_name = Str(required=True)
    family_name = Str(required=True)


class SignUpSchema(Schema):
    body = Nested(SignUpBody, required=True)

    @pre_load
    def input(self, event: dict, **kwargs):
        payload = {}

        if event.get("body"):
            payload["body"] = json.loads(event["body"])

        return payload
