from application.controllers.user.find_user import FindUser
from common.core import make_handler
from common.decorators import response_json


@response_json
def handler(event, _):
    routes = {
        ("GET", "/users/{user_id}"): FindUser.process,
    }

    response = make_handler(event, routes)

    return response
