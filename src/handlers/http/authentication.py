from application.controllers.authentication.account_confirmation import \
    AccountConfirmationController
from application.controllers.authentication.forgot_password import \
    ForgotPasswordController
from application.controllers.authentication.sign_in import SignInController
from application.controllers.authentication.sign_up import SignUpController
from common.core import make_handler
from common.decorators import response_json


@response_json
def handler(event: dict, _) -> dict:
    routes = {
        ("GET", "/auth/profile"): None,
        ("POST", "/auth/sign-up"): SignUpController.process,
        ("POST", "/auth/sign-in"): SignInController.process,
        ("POST", "/auth/account-confirmation"): AccountConfirmationController.process,
        ("POST", "/auth/reset-password"): None,
        ("POST", "/auth/forgot-password"): ForgotPasswordController.process,
        ("POST", "/auth/refresh-token"): None,
    }

    response = make_handler(event, routes)

    return response
