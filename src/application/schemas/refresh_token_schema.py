import json

from marshmallow import Schema, pre_load
from marshmallow.fields import Nested, Str


class RefreshTokenBody(Schema):
    user_token = Str(required=True, description="user auth token")


class RefreshTokenSchema(Schema):
    body = Nested(RefreshTokenBody, required=True)

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
