import uuid
from decimal import Decimal
from typing import Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict


class Order(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: uuid.UUID
    symbol: Literal["BTC-USDT", "ETH-USDT"]
    side: Literal["BUY", "SELL"]
    type: Literal["LIMIT"]
    price: Decimal
    quantity: Decimal
    filled_quantity: Decimal
    status: Literal["NEW", "PARTIALLY_FILLED", "FILLED", "CANCELED"]
    created_at: AwareDatetime
    updated_at: AwareDatetime
