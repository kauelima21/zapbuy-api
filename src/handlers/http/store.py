from application.controllers.store.admin_fetch_store_products import \
    AdminFetchStoreProductsController
from application.controllers.store.fetch_store_products import \
    FetchStoreProductsController
from application.controllers.store.find_product import FindProduct
from common.core import make_handler
from common.decorators import response_json


@response_json
def handler(event, _):
    routes = {
        ("GET", "/stores/{slug}/products"): FetchStoreProductsController.process,
        ("GET", "/stores/{slug}/products/{product_id}"): FindProduct.process,
        ("GET", "/admin/stores/{slug}/products"): AdminFetchStoreProductsController.process,
    }

    response = make_handler(event, routes)

    return response
