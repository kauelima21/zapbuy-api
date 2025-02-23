def make_handler(event: dict, routes: dict) -> dict:
    route_key = event["routeKey"].split()
    http_method = route_key[0]
    path = route_key[1]

    handler = routes.get((http_method, path))
    return handler(event)
