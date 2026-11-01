import uuid
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict


class CreateOrder(BaseModel):
    """Тело POST /orders. Суммы — строки, как их ждёт API. Им же пользуются UI-тесты."""

    symbol: str = "ETH-USDT"
    side: str = "BUY"
    type: str = "LIMIT"
    price: str = "1"
    quantity: str = "1"

    @property
    def cost(self) -> Decimal:
        return Decimal(self.price) * Decimal(self.quantity)


class Order(BaseModel):
    """Ответ /orders: точные типы, лишние поля запрещены."""

    model_config = ConfigDict(extra="forbid")

    id: uuid.UUID
    symbol: Literal["BTC-USDT", "ETH-USDT"]
    side: Literal["BUY", "SELL"]
    type: Literal["LIMIT", "MARKET"]
    price: Decimal
    quantity: Decimal
    filled_quantity: Decimal
    status: Literal["NEW", "FILLED", "PARTIALLY_FILLED", "CANCELED"]
    created_at: datetime
    updated_at: datetime
