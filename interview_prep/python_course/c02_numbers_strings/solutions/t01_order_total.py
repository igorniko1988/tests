from decimal import ROUND_HALF_UP, Decimal


def order_total(lines: list[tuple[str, int]], fee_percent: str = "0") -> str:
    total = sum((Decimal(price) * qty for price, qty in lines), Decimal("0"))
    total += total * Decimal(fee_percent) / 100
    return str(total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


# sum(..., Decimal("0")) — стартовое значение Decimal, иначе на пустом списке вернётся int 0
# и quantize не сработает.
