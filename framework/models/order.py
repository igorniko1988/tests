from pydantic import BaseModel, ConfigDict

class Order(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)

    id: str
    symbol: str
    side: str
    type: str
    type: str
    price: str
    quantity: str
    filled_quantity: str
    status: str
    created_at: str
    updated_at: str
