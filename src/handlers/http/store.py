from application.controllers.store.admin_fetch_store_products_controller import \
    AdminFetchStoreProductsController
from application.controllers.store.admin_fetch_stores_controller import \
    AdminFetchStoresController
from application.controllers.store.fetch_store_products_controller import \
    FetchStoreProductsController
from application.controllers.store.find_product_controller import FindProductController
from application.controllers.store.find_store_controller import FindStoreController
from application.controllers.store.save_store_controller import SaveStoreController
from common.core import make_handler
from common.decorators import response_json


@response_json
def handler(event, _):
    routes = {
        ("GET", "/stores/{slug}/products"): FetchStoreProductsController.process,
        ("GET", "/stores/{slug}/products/{product_id}"): FindProductController.process,
        ("GET", "/admin/stores/{slug}/products"): AdminFetchStoreProductsController.process,
        ("GET", "/stores/{slug}"): FindStoreController.process,
        ("POST", "/admin/stores"): SaveStoreController.process,
        ("GET", "/admin/{owner_id}/stores"): AdminFetchStoresController.process,
    }

    response = make_handler(event, routes)

    return response
