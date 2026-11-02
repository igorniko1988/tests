from functools import partial


def build_client(request) -> dict:
    return {
        "get_user": partial(request, "GET", "users"),
        "get_order": partial(request, "GET", "orders"),
        "create_order": partial(request, "POST", "orders", timeout=10),
        "health": partial(request, "GET", "health", timeout=1),
    }
