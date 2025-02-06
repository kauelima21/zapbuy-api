import json

from marshmallow import Schema, pre_load
from marshmallow.fields import Nested, Str


class SignUpBody(Schema):
    email = Str(required=True, description="user email")
    password = Str(required=True, description="user password")
    password_confirm = Str(required=True, description="password confirmation")
    first_name = Str(required=True, description="user first name")
    last_name = Str(required=True, description="user last name")


class SignUpSchema(Schema):
    body = Nested(SignUpBody, required=True)

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
