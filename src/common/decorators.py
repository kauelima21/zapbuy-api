import json
from functools import wraps


def response_json(handler):
    @wraps(handler)
    def transform_response(*args, **kwargs):
        response = handler(*args, **kwargs)
        return {
            "statusCode": response["status_code"],
            "body": json.dumps(response.get("body")),
            "isBase64Encoded": False,
            "headers": {"Content-Type": "application/json"},
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
