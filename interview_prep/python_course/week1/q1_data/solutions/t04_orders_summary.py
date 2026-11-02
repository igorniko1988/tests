from decimal import ROUND_HALF_UP, Decimal


def orders_summary(orders: list[dict]) -> dict[str, dict]:
    counts, totals = {}, {}
    for order in orders:
        status = order["status"]
        counts[status] = counts.get(status, 0) + 1
        totals[status] = totals.get(status, Decimal("0")) + Decimal(order["amount"])
    return {
        status: {
            "count": counts[status],
            "total": str(totals[status].quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
        }
        for status in counts
    }
