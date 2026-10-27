import uuid
from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, PlainSerializer

from exchange.db import OrderSide, OrderStatus, OrderType

ASSETS = ("BTC", "ETH", "USDT")
SYMBOLS = {"BTC-USDT": ("BTC", "USDT"), "ETH-USDT": ("ETH", "USDT")}


def _format_amount(value: Decimal) -> str:
    # Суммы отдаём строкой, как биржи: float теряет точность
    return format(value.normalize(), "f") if value else "0"


Amount = Annotated[Decimal, PlainSerializer(_format_amount, return_type=str, when_used="json")]
PositiveAmount = Annotated[
    Decimal,
    Field(gt=0, max_digits=36, decimal_places=18),
    PlainSerializer(_format_amount, return_type=str, when_used="json"),
]


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    created_at: datetime


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int


class BalanceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    asset: str
    available: Amount
    locked: Amount


class DepositRequest(BaseModel):
    asset: str = Field(pattern="^(BTC|ETH|USDT)$")
    amount: PositiveAmount


class CreateOrderRequest(BaseModel):
    symbol: str = Field(pattern="^(BTC-USDT|ETH-USDT)$")
    side: OrderSide
    type: OrderType = OrderType.LIMIT
    price: PositiveAmount
    quantity: PositiveAmount


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    symbol: str
    side: OrderSide
    type: OrderType
    price: Amount
    quantity: Amount
    filled_quantity: Amount
    status: OrderStatus
    created_at: datetime
    updated_at: datetime


class CreateWebhookRequest(BaseModel):
    url: str = Field(pattern="^https?://", max_length=2048)


class WebhookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    url: str
    secret: str
    created_at: datetime
