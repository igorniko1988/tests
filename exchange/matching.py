"""Фоновое сопоставление ордеров: BUY и SELL с пересекающейся ценой исполняются.

Работает раз в settings.matching_interval секунд, поэтому исполнение видно
не сразу после создания ордера — это и есть eventual consistency.
Цена сделки — цена более раннего ордера (maker).
"""

import asyncio
import logging
from decimal import Decimal

from sqlalchemy import select

from exchange.api.balances import lock_balance
from exchange.config import settings
from exchange.db import Order, OrderSide, OrderStatus, SessionLocal
from exchange.schemas import SYMBOLS

log = logging.getLogger(__name__)
OPEN = (OrderStatus.NEW, OrderStatus.PARTIALLY_FILLED)


async def _best(session, symbol: str, side: OrderSide) -> Order | None:
    price_order = Order.price.desc() if side is OrderSide.BUY else Order.price.asc()
    query = (
        select(Order)
        .where(Order.symbol == symbol, Order.side == side, Order.status.in_(OPEN))
        .order_by(price_order, Order.created_at)
        .limit(1)
        .with_for_update()
    )
    return await session.scalar(query)


def _fill(order: Order, qty: Decimal) -> None:
    order.filled_quantity += qty
    order.status = (
        OrderStatus.FILLED
        if order.filled_quantity == order.quantity
        else OrderStatus.PARTIALLY_FILLED
    )


async def _trade(session, buy: Order, sell: Order) -> None:
    base, quote = SYMBOLS[buy.symbol]
    qty = min(buy.quantity - buy.filled_quantity, sell.quantity - sell.filled_quantity)
    price = buy.price if buy.created_at <= sell.created_at else sell.price

    buyer_quote = await lock_balance(session, buy.user_id, quote)
    buyer_base = await lock_balance(session, buy.user_id, base)
    seller_base = await lock_balance(session, sell.user_id, base)
    seller_quote = await lock_balance(session, sell.user_id, quote)

    # Покупатель блокировал по своей цене, платит по цене сделки, разницу получает обратно
    buyer_quote.locked -= qty * buy.price
    buyer_quote.available += qty * (buy.price - price)
    buyer_base.available += qty
    seller_base.locked -= qty
    seller_quote.available += qty * price

    _fill(buy, qty)
    _fill(sell, qty)


async def match_once() -> None:
    async with SessionLocal() as session:
        for symbol in SYMBOLS:
            while True:
                buy = await _best(session, symbol, OrderSide.BUY)
                sell = await _best(session, symbol, OrderSide.SELL)
                if buy is None or sell is None or buy.price < sell.price:
                    break
                await _trade(session, buy, sell)
                await session.flush()
        await session.commit()


async def run_matching() -> None:
    while True:
        try:
            await match_once()
        except Exception:
            log.exception("matching failed")
        await asyncio.sleep(settings.matching_interval)
