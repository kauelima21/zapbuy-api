from application.controllers.authentication.account_confirmation_controller import \
    AccountConfirmationController
from application.controllers.authentication.forgot_password_controller import \
    ForgotPasswordController
from application.controllers.authentication.generate_confirmation_code_controller import \
    GenerateConfirmationCodeController
from application.controllers.authentication.profile_controller import ProfileController
from application.controllers.authentication.profile_update_controller import ProfileUpdateController
from application.controllers.authentication.refresh_token_controller import \
    RefreshTokenController
from application.controllers.authentication.reset_password_controller import \
    ResetPasswordController
from application.controllers.authentication.sign_in_controller import SignInController
from application.controllers.authentication.sign_up_controller import SignUpController
from common.core import make_handler
from common.decorators import response_json


@response_json(log_event=True)
def handler(event: dict, _) -> dict:
    routes = {
        ("GET", "/auth/profile"): ProfileController.process,
        ("PUT", "/auth/profile"): ProfileUpdateController.process,
        ("POST", "/auth/sign-up"): SignUpController.process,
        ("POST", "/auth/sign-in"): SignInController.process,
        ("POST", "/auth/account-confirmation"): AccountConfirmationController.process,
        ("POST", "/auth/generate-confirmation-code"): GenerateConfirmationCodeController.process,
        ("POST", "/auth/reset-password"): ResetPasswordController.process,
        ("POST", "/auth/forgot-password"): ForgotPasswordController.process,
        ("POST", "/auth/refresh-token"): RefreshTokenController.process,
    }

    response = make_handler(event, routes)

    return response
