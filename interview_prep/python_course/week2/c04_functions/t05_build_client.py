"""C4 t05 (required, ~15 min). API helpers with functools.partial.

There is one generic function that sends requests:

    request(method, resource, item_id=None, *, timeout=5, **body)

Implement build_client(request) that returns a dict of ready-made helpers,
each created with functools.partial (the test checks the type):

    "get_user"     -> request("GET", "users", <user_id>)
    "get_order"    -> request("GET", "orders", <order_id>)
    "create_order" -> request("POST", "orders", timeout=10, **<body>)
    "health"       -> request("GET", "health", timeout=1)

Example:
    client = build_client(request)
    client["get_user"](7)                  # calls request("GET", "users", 7)
    client["create_order"](symbol="BTC")   # calls request("POST", "orders", timeout=10, symbol="BTC")
    client["health"]()                     # calls request("GET", "health", timeout=1)

Every helper returns whatever request returned.

Follow-up questions:
- What is the difference between partial and a lambda here?
- How do you see which arguments a partial already holds?

Run (from interview_prep/python_course/week2/c04_functions): uv run pytest -k t05
Теория: THEORY.md в этой папке, раздел 9.
"""


from functools import partial  # noqa: F401


def build_client(request) -> dict:
    raise NotImplementedError
