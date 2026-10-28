from dataclasses import dataclass
from decimal import Decimal

from ui_framework.utils.money import to_decimal


@dataclass(frozen=True)
class OrderData:
    side: str = 'BUY'
    price: str = '1'
    quantity: str = '1'
    symbol: str = 'ETH-USDT'

    @property
    def cost(self) -> Decimal:
        return to_decimal(self.quantity) * to_decimal(self.price)
