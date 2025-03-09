import json

from marshmallow import Schema, pre_load
from marshmallow.fields import Nested, Str


class GenerateConfirmationCodeBody(Schema):
    email = Str(required=True)


class GenerateConfirmationCodeSchema(Schema):
    body = Nested(GenerateConfirmationCodeBody, required=True)

    @pre_load
    def input(self, event: dict, **kwargs):
        payload = {}

        if event.get("body"):
            payload["body"] = json.loads(event["body"])

        return payload
