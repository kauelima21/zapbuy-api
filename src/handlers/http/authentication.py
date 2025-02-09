from application.controllers.authentication.sign_in import SignInController
from application.controllers.authentication.sign_up import SignUpController
from common.core import make_handler
from common.decorators import response_json


@response_json
def handler(event: dict, _):
    routes = {
        ("GET", "/auth/profile"): None,
        ("POST", "/auth/sign-up"): SignUpController.process,
        ("POST", "/auth/sign-in"): SignInController.process,
        ("POST", "/auth/account-confirmation"): None,
        ("POST", "/auth/reset-password"): None,
        ("POST", "/auth/forgot-password"): None,
        ("POST", "/auth/refresh-token"): None,
    }

    response = make_handler(event, routes)

    return response
