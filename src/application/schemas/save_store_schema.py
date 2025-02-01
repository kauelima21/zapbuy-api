import json

from marshmallow import Schema, pre_load
from marshmallow.fields import Nested, Str


class WorkDays(Schema):
    start_day = Str(required=True, description="first work week day")
    last_day = Str(required=True, description="last work week day")


class WorkHours(Schema):
    start_hour = Str(required=True, description="first work hour")
    last_hour = Str(required=True, description="last work hour")


class SaveStoreBody(Schema):
    store_name = Str(required=True, description="store name")
    owner_id = Str(required=True, description="store owner id")
    whatsapp_number = Str(required=True, description="whatsapp number")
    work_days = Nested(WorkDays, required=True)
    work_hours = Nested(WorkHours, required=True)


class SaveStoreSchema(Schema):
    body = Nested(SaveStoreBody, required=True)

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
