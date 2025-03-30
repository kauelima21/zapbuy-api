from application.controllers.category.admin_fetch_categories_controller import AdminFetchCategoriesController
from application.controllers.category.fetch_categories_controller import FetchCategoriesController
from application.controllers.category.save_category_controller import SaveCategoryController
from application.controllers.category.update_category_controller import UpdateCategoryController
from common.core import make_handler
from common.decorators import response_json


@response_json(log_event=False)
def handler(event: dict, _) -> dict:
    routes = {
        ("GET", "/stores/{slug}/categories"): FetchCategoriesController.process,
        ("PUT", "/admin/stores/{slug}/categories/{category_id}"): UpdateCategoryController.process,
        ("POST", "/admin/stores/{slug}/categories"): SaveCategoryController.process,
        ("GET", "/admin/stores/{slug}/categories"): AdminFetchCategoriesController.process,
    }

    response = make_handler(event, routes)

    return response
