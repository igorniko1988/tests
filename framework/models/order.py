from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime
from typing import Literal
from decimal import Decimal


class CreateOrder(BaseModel):
    symbol: str = 'ETH-USDT'
    side: str = 'BUY'
    type: str = 'LIMIT'
    price: str = '1'
    quantity: str = '1'


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
