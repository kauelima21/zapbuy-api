from marshmallow import Schema, pre_load, EXCLUDE
from marshmallow.fields import Nested, Str, Int


class AdminFetchCategoriesClaims(Schema):
    sub = Str(required=True)

    class Meta:
        unknown = EXCLUDE


class AdminFetchCategoriesAuthorizerJwt(Schema):
    claims = Nested(AdminFetchCategoriesClaims, required=True)

    class Meta:
        unknown = EXCLUDE


class AdminFetchCategoriesAuthorizer(Schema):
    jwt = Nested(AdminFetchCategoriesAuthorizerJwt, required=True)

    class Meta:
        unknown = EXCLUDE


class HttpRequestContext(Schema):
    method = Str(required=True)

    class Meta:
        unknown = EXCLUDE


class AdminFetchCategoriesRequestContex(Schema):
    authorizer = Nested(AdminFetchCategoriesAuthorizer, required=True)
    http = Nested(HttpRequestContext, required=True)

    class Meta:
        unknown = EXCLUDE


class AdminFetchCategoriesParams(Schema):
    slug = Str(required=True)


class AdminFetchCategoriesSchema(Schema):
    params = Nested(AdminFetchCategoriesParams, required=True)
    request_context = Nested(AdminFetchCategoriesRequestContex, required=True)

    @pre_load
    def input(self, event: dict, **kwargs):
        payload = {}

        if event.get("pathParameters"):
            payload["params"] = event["pathParameters"]

        if event.get("requestContext"):
            payload["request_context"] = event["requestContext"]

        return payload
