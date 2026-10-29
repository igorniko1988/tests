from collections import defaultdict


def group_orders(orders: list[dict]) -> dict[str, list[int]]:
    groups = defaultdict(list)
    for order in orders:
        groups[order["status"]].append(order["id"])
    return dict(groups)
