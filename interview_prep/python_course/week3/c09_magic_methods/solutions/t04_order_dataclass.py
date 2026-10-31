from dataclasses import asdict, dataclass, field
from decimal import Decimal


@dataclass
class Order:
    symbol: str
    side: str
    qty: int = 1
    price: Decimal = Decimal("0")
    tags: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.side = self.side.upper()
        if self.side not in ("BUY", "SELL"):
            raise ValueError(f"bad side: {self.side!r}")
        if self.qty <= 0:
            raise ValueError("qty must be positive")
        if isinstance(self.price, float):
            raise TypeError("price must not be float")
        self.price = Decimal(self.price)

    def to_payload(self) -> dict:
        payload = asdict(self)
        payload["price"] = str(self.price)
        return payload
