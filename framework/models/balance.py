from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class Balance(BaseModel):
    model_config = ConfigDict(extra="forbid")

    asset: str
    available: Decimal
    locked: Decimal
