import json

from marshmallow import Schema, pre_load
from marshmallow.fields import Nested, Str


class WorkDays(Schema):
    start_day = Str(required=True)
    last_day = Str(required=True)


class WorkHours(Schema):
    start_hour = Str(required=True)
    last_hour = Str(required=True)


class SaveStoreBody(Schema):
    store_name = Str(required=True)
    owner_id = Str(required=True)
    whatsapp_number = Str(required=True)
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
