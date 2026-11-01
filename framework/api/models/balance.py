from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict


class Balance(BaseModel):
    model_config = ConfigDict(extra="forbid")

    asset: Literal["BTC", "ETH", "USDT"]
    available: Decimal
    locked: Decimal
