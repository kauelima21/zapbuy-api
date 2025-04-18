from application.controllers.store.admin_fetch_stores_controller import \
    AdminFetchStoresController
from application.controllers.store.find_store_controller import FindStoreController
from application.controllers.store.save_store_controller import SaveStoreController
from common.core import make_handler
from common.decorators import response_json


@response_json(log_event=True)
def handler(event: dict, _) -> dict:
    routes = {
        ("GET", "/stores/{slug}"): FindStoreController.process,
        ("POST", "/admin/stores"): SaveStoreController.process,
        ("GET", "/admin/stores"): AdminFetchStoresController.process,
    }

    response = make_handler(event, routes)

    return response
