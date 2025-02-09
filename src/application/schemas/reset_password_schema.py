import json

from marshmallow import Schema, pre_load
from marshmallow.fields import Nested, Str


class ResetPasswordBody(Schema):
    email = Str(required=True, description="user email")
    password = Str(required=True, description="user new password")
    confirmation_code = Str(required=True, description="reset password code")


class ResetPasswordSchema(Schema):
    body = Nested(ResetPasswordBody, required=True)

    @pre_load
    def input(self, event: dict, **kwargs):
        payload = {}

        if event.get("pathParameters"):
            payload["params"] = event["pathParameters"]

        if event.get("queryStringParams"):
            payload["query"] = event["queryStringParams"]

        if event.get("body"):
            payload["body"] = json.loads(event["body"])

        return payload
