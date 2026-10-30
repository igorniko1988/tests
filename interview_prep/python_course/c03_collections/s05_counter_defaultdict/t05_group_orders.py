"""C3 t05 (required, ~10 min). Group orders by status.

Given a list of orders like {"id": 1, "status": "NEW"}, return a dict
that maps each status to the list of order ids with that status.

Requirements:
- Ids inside each list keep the input order.
- Statuses appear in the order of their first occurrence.
- Return a plain dict (the test checks type(result) is dict).
- Do not modify the input list.

Example:
    orders = [
        {"id": 1, "status": "NEW"},
        {"id": 2, "status": "FILLED"},
        {"id": 3, "status": "NEW"},
    ]
    group_orders(orders) -> {"NEW": [1, 3], "FILLED": [2]}
    group_orders([])     -> {}

Follow-up questions:
- Why defaultdict(list) and not defaultdict([])?
- Why convert to dict(...) if a defaultdict compares equal to a dict anyway?

Run: uv run pytest -k t05
Теория: THEORY.md в этой папке, раздел 5.
"""


def group_orders(orders: list[dict]) -> dict[str, list[int]]:
    raise NotImplementedError
