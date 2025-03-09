import json

from marshmallow import Schema, pre_load
from marshmallow.fields import Nested, Str


class AccountConfirmationBody(Schema):
    email = Str(required=True)
    confirmation_code = Str(required=True)


class AccountConfirmationSchema(Schema):
    body = Nested(AccountConfirmationBody, required=True)

    @pre_load
    def input(self, event: dict, **kwargs):
        payload = {}

        if event.get("body"):
            payload["body"] = json.loads(event["body"])

        return payload
