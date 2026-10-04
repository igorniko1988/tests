import uuid
from decimal import Decimal

from fastapi import APIRouter
from sqlalchemy import select

from exchange.api.balances import lock_balance
from exchange.api.deps import Session, UserId
from exchange.db import Order, OrderSide, OrderStatus
from exchange.errors import ApiError
from exchange.schemas import SYMBOLS, CreateOrderRequest, OrderOut

router = APIRouter(tags=["orders"])

OPEN_STATUSES = (OrderStatus.NEW, OrderStatus.PARTIALLY_FILLED)


def _funds_to_lock(order: Order) -> tuple[str, object]:
    base, quote = SYMBOLS[order.symbol]
    remaining = order.quantity - order.filled_quantity
    if order.side is OrderSide.BUY:
        return quote, remaining * order.price
    return base, remaining


@router.post("/orders", status_code=201, response_model=OrderOut)
async def create_order(body: CreateOrderRequest, user_id: UserId, session: Session):
    order = Order(user_id=user_id, filled_quantity=Decimal(0), **body.model_dump())
    asset, amount = _funds_to_lock(order)
    balance = await lock_balance(session, user_id, asset)
    if balance.available < amount:
        await session.rollback()
        raise ApiError(400, "insufficient_funds", f"Not enough {asset} to place order")
    balance.available -= amount
    balance.locked += amount
    session.add(order)
    await session.commit()
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
    return order
