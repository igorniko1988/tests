"""Подписанные запросы, как в API бирж (Binance).

Ключ: POST /api-keys → {key, secret}. Запрос к /v1/*: заголовок X-API-KEY, параметры в query,
последним — signature = HMAC-SHA256(secret, query без signature) в hex.
Обязательный timestamp (мс); запрос старше recvWindow (мс, по умолчанию 5000) или из будущего
больше чем на 1 с отклоняется. Время сервера — GET /time.
"""

import hashlib
import hmac
import secrets
import time
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Header, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from exchange.api.balances import list_balances
from exchange.api.deps import Session, UserId
from exchange.api.orders import create_order
from exchange.db import ApiKey
from exchange.errors import ApiError
from exchange.schemas import ApiKeyOut, BalanceOut, CreateOrderRequest, OrderOut

router = APIRouter(tags=["signed"])

DEFAULT_RECV_WINDOW = 5000
MAX_CLOCK_AHEAD = 1000


def _now_ms() -> int:
    return int(time.time() * 1000)


@router.get("/time")
async def server_time():
    return {"serverTime": _now_ms()}


@router.post("/api-keys", status_code=201, response_model=ApiKeyOut)
async def create_api_key(user_id: UserId, session: Session):
    api_key = ApiKey(key=secrets.token_hex(16), secret=secrets.token_hex(32), user_id=user_id)
    session.add(api_key)
    await session.commit()
    return api_key


async def signed_user_id(
    request: Request,
    session: Session,
    x_api_key: Annotated[str | None, Header()] = None,
) -> uuid.UUID:
    if not x_api_key:
        raise ApiError(401, "api_key_required", "X-API-KEY header is required")
    api_key = await session.get(ApiKey, x_api_key)
    if api_key is None:
        raise ApiError(401, "invalid_api_key", "Unknown API key")

    params = request.query_params
    signature = params.get("signature")
    if not signature or "timestamp" not in params:
        raise ApiError(400, "signature_required", "timestamp and signature are required")
    payload = "&".join(p for p in request.url.query.split("&") if not p.startswith("signature="))
    expected = hmac.new(api_key.secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise ApiError(401, "invalid_signature", "Signature does not match")

    try:
        timestamp = int(params["timestamp"])
        recv_window = int(params.get("recvWindow", DEFAULT_RECV_WINDOW))
    except ValueError:
        message = "timestamp and recvWindow must be integers"
        raise ApiError(400, "invalid_timestamp", message) from None
    now = _now_ms()
    if timestamp > now + MAX_CLOCK_AHEAD:
        raise ApiError(400, "timestamp_ahead", "Timestamp is ahead of the server time")
    if now - timestamp > recv_window:
        raise ApiError(400, "timestamp_outside_recv_window", "Timestamp is outside of recvWindow")
    return api_key.user_id


SignedUserId = Annotated[uuid.UUID, Depends(signed_user_id)]


@router.get("/v1/account", response_model=list[BalanceOut])
async def signed_account(user_id: SignedUserId, session: Session):
    return await list_balances(user_id, session)


@router.post("/v1/orders", status_code=201, response_model=OrderOut)
async def signed_create_order(request: Request, user_id: SignedUserId, session: Session):
    fields = ("symbol", "side", "type", "price", "quantity")
    data = {f: request.query_params[f] for f in fields if f in request.query_params}
    try:
        body = CreateOrderRequest(**data)
    except ValidationError as error:
        raise RequestValidationError(
            [{**e, "loc": ("query", *e["loc"])} for e in error.errors()]
        ) from None
    return await create_order(body, user_id, session, None)
