from decimal import Decimal


class Order:
    def __init__(self, order_id: int, symbol: str, side: str, qty: int, price) -> None:
        side = side.upper()
        if side not in ("BUY", "SELL"):
            raise ValueError(f"bad side: {side!r}")
        self.order_id = order_id
        self.symbol = symbol
        self.side = side
        self.qty = qty
        self.price = Decimal(price)

    @classmethod
    def from_json(cls, data: dict):
        return cls(int(data["id"]), data["symbol"], data["side"], int(data["qty"]), Decimal(data["price"]))

    @property
    def total(self) -> Decimal:
        return self.qty * self.price
