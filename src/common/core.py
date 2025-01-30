def make_handler(event: dict, routes: dict):
    http_method = event.get("httpMethod")
    path = event.get("path")

    handler = routes.get((http_method, path))
    return handler(event)
