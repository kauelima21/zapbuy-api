def make_handler(event: dict, routes: dict) -> dict:
    http_method = event.get("requestContext", {}).get("http", {}).get("method")
    path = event.get("rawPath")

    handler = routes.get((http_method, path))
    return handler(event)
