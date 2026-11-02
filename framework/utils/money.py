from decimal import Decimal


def to_decimal(value: str | int | Decimal) -> Decimal:
    return Decimal(str(value))


def format_amount(value: str | int | Decimal) -> str:
    d = to_decimal(value)
    return format(d.normalize(), "f") if d else "0"