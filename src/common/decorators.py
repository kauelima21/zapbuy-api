import json
from functools import wraps

from common.errors import BaseError


def response_json(handler):
    @wraps(handler)
    def transform_response(*args, **kwargs):
        response_dict = {
            "isBase64Encoded": False,
            "headers": {"Content-Type": "application/json"},
        }

        try:
            response = handler(*args, **kwargs)
        except BaseError as error:
            response = {"status_code": error.status_code,
                        "body": error.to_dict()}

        return {
            **response_dict,
            "statusCode": response["status_code"],
            "body": json.dumps(response.get("body")),
        }

    return transform_response


def load_schema(schema):
    def decorator_schema(handler):
        @wraps(handler)
        def wrapper(*args, **kwargs):
            payload = schema().load(args[0])
            return handler(payload)

        return wrapper

    return decorator_schema
