import hashlib
import uuid
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Header
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from exchange.api.balances import lock_balance
from exchange.api.deps import Session, UserId
from exchange.db import IdempotencyKey, Order, OrderSide, OrderStatus, OrderType
from exchange.errors import ApiError
from exchange.events import build_event, send
from exchange.orderbook import publish
from exchange.pricefeed import current_price
from exchange.schemas import SYMBOLS, CreateOrderRequest, OrderOut
from exchange.webhooks import notify

router = APIRouter(tags=["orders"])

OPEN_STATUSES = (OrderStatus.NEW, OrderStatus.PARTIALLY_FILLED)


def _check_price(body: CreateOrderRequest) -> None:
    needs_price = body.type is OrderType.LIMIT
    if needs_price == (body.price is not None):
        return
    message = "Field required" if needs_price else "Price must not be set for MARKET order"
    raise RequestValidationError(
        [{"loc": ("body", "price"), "msg": message, "type": "value_error"}]
    )


def _funds_to_lock(order: Order) -> tuple[str, object]:
    base, quote = SYMBOLS[order.symbol]
    remaining = order.quantity - order.filled_quantity
    if order.side is OrderSide.BUY:
        return quote, remaining * order.price
    return base, remaining


async def _find_key(session, user_id: uuid.UUID, key: str) -> IdempotencyKey | None:
    query = select(IdempotencyKey).where(
        IdempotencyKey.user_id == user_id, IdempotencyKey.key == key
    )
    return await session.scalar(query)


def _replay(saved: IdempotencyKey, request_hash: str) -> JSONResponse:
    if saved.request_hash != request_hash:
        raise ApiError(
            422, "idempotency_key_reused", "Idempotency-Key was used with a different request"
        )
    return JSONResponse(status_code=saved.status_code, content=saved.response_body)


@router.post("/orders", status_code=201, response_model=OrderOut)
async def create_order(
    body: CreateOrderRequest,
    user_id: UserId,
    session: Session,
    idempotency_key: Annotated[str | None, Header(max_length=255)] = None,
):
    _check_price(body)
    request_hash = hashlib.sha256(body.model_dump_json().encode()).hexdigest()
    if idempotency_key:
        saved = await _find_key(session, user_id, idempotency_key)
        if saved:
            return _replay(saved, request_hash)

    order = Order(user_id=user_id, filled_quantity=Decimal(0), **body.model_dump())
    if body.type is OrderType.MARKET:
        # Дальше MARKET-ордер живёт в стакане как лимитный по цене провайдера
        order.price = await current_price(body.symbol)
    asset, amount = _funds_to_lock(order)
    balance = await lock_balance(session, user_id, asset)
    if balance.available < amount:
        await session.rollback()
        raise ApiError(400, "insufficient_funds", f"Not enough {asset} to place order")
    balance.available -= amount
    balance.locked += amount
    session.add(order)
    await session.flush()

    if idempotency_key:
        session.add(
            IdempotencyKey(
                user_id=user_id,
                key=idempotency_key,
                request_hash=request_hash,
                status_code=201,
                response_body=OrderOut.model_validate(order).model_dump(mode="json"),
            )
        )
    try:
        await session.commit()
    except IntegrityError:
        # Такой же запрос с этим ключом успел раньше: наш откатился целиком
        await session.rollback()
        return _replay(await _find_key(session, user_id, idempotency_key), request_hash)
    await send(build_event(order, "order.created"))
    await publish(order.symbol)
    return order


@router.get("/orders", response_model=list[OrderOut])
async def list_orders(user_id: UserId, session: Session, status: OrderStatus | None = None):
    query = select(Order).where(Order.user_id == user_id).order_by(Order.created_at.desc())
    if status is not None:
        query = query.where(Order.status == status)
    return list(await session.scalars(query))


async def _get_own_order(session, order_id: uuid.UUID, user_id: uuid.UUID, lock=False) -> Order:
    query = select(Order).where(Order.id == order_id, Order.user_id == user_id)
    if lock:
        query = query.with_for_update()
    order = await session.scalar(query)
    if order is None:
        raise ApiError(404, "order_not_found", "Order not found")
    return order


@router.get("/orders/{order_id}", response_model=OrderOut)
async def get_order(order_id: uuid.UUID, user_id: UserId, session: Session):
    return await _get_own_order(session, order_id, user_id)


@router.delete("/orders/{order_id}", response_model=OrderOut)
async def cancel_order(order_id: uuid.UUID, user_id: UserId, session: Session):
    order = await _get_own_order(session, order_id, user_id, lock=True)
    if order.status not in OPEN_STATUSES:
        raise ApiError(409, "order_not_open", f"Order is already {order.status}")
    asset, amount = _funds_to_lock(order)
    balance = await lock_balance(session, user_id, asset)
    balance.locked -= amount
    balance.available += amount
    order.status = OrderStatus.CANCELED
    await session.commit()
    await publish(order.symbol)
    notify(order, "order.canceled")
    await send(build_event(order, "order.canceled"))
    return order
