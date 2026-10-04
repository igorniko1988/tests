import uuid
from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class OrderSide(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(StrEnum):
    LIMIT = "LIMIT"


class OrderStatus(StrEnum):
    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"


class Order(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: uuid.UUID
    symbol: str
    side: OrderSide
    type: OrderType
    price: Decimal
    quantity: Decimal
    filled_quantity: Decimal
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
