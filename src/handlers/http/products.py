from application.controllers.product.admin_fetch_store_products_controller import \
    AdminFetchStoreProductsController
from application.controllers.product.fetch_store_products_controller import \
    FetchStoreProductsController
from application.controllers.product.find_product_controller import FindProductController
from application.controllers.product.save_product_controller import \
    SaveProductController
from common.core import make_handler
from common.decorators import response_json


@response_json
def handler(event: dict, _) -> dict:
    routes = {
        ("GET", "/stores/{slug}/products"): FetchStoreProductsController.process,
        ("GET", "/stores/{slug}/products/{product_id}"): FindProductController.process,
        ("GET", "/admin/stores/{slug}/products"): AdminFetchStoreProductsController.process,
        ("POST", "/admin/stores/{slug}/products"): SaveProductController.process,
    }

    response = make_handler(event, routes)

    return response
