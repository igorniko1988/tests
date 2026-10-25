from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime
from typing import Literal
from decimal import Decimal

class Order(BaseModel):
    model_config = ConfigDict(extra='forbid')

    id: uuid.UUID
    symbol: Literal['BTC-USDT','ETH-USDT']
    side: Literal['BUY','SELL']
    type: Literal['LIMIT']
    price: Decimal
    quantity: Decimal
    filled_quantity: Decimal
    status: Literal['NEW','FILLED','PARTIALLY_FILLED','CANCELED']
    created_at: datetime
    updated_at: datetime
