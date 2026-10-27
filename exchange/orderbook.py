"""Стакан ордеров в реальном времени по WebSocket.

При подключении клиент получает snapshot, дальше — update после каждого
изменения стакана. У каждого сообщения есть sequence: по нему клиент видит,
что ничего не пропустил (номера идут подряд).
"""

import asyncio
from collections import defaultdict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import func, select

from exchange.db import Order, OrderSide, OrderStatus, SessionLocal
from exchange.schemas import SYMBOLS, _format_amount

router = APIRouter(tags=["websocket"])

OPEN = (OrderStatus.NEW, OrderStatus.PARTIALLY_FILLED)
DEPTH = 20

subscribers: dict[str, set[asyncio.Queue]] = defaultdict(set)
sequence: dict[str, int] = defaultdict(int)


async def build_book(symbol: str) -> dict:
    async with SessionLocal() as session:
        remaining = func.sum(Order.quantity - Order.filled_quantity)
        book = {}
        for side, key, ordering in (
            (OrderSide.BUY, "bids", Order.price.desc()),
            (OrderSide.SELL, "asks", Order.price.asc()),
        ):
            query = (
                select(Order.price, remaining)
                .where(Order.symbol == symbol, Order.side == side, Order.status.in_(OPEN))
                .group_by(Order.price)
                .order_by(ordering)
                .limit(DEPTH)
            )
            rows = await session.execute(query)
            book[key] = [[_format_amount(price), _format_amount(qty)] for price, qty in rows]
        return book


async def publish(symbol: str) -> None:
    """Сообщить подписчикам, что стакан symbol изменился."""
    sequence[symbol] += 1
    message = {"type": "update", "symbol": symbol, "sequence": sequence[symbol]}
    message |= await build_book(symbol)
    for queue in subscribers[symbol]:
        queue.put_nowait(message)


@router.websocket("/ws/orderbook/{symbol}")
async def orderbook_stream(websocket: WebSocket, symbol: str):
    # Сначала accept: закрытие до него uvicorn превращает в HTTP 403 на рукопожатии
    await websocket.accept()
    if symbol not in SYMBOLS:
        await websocket.close(code=4004, reason="Unknown symbol")
        return
    queue: asyncio.Queue = asyncio.Queue()
    subscribers[symbol].add(queue)
    try:
        snapshot = {"type": "snapshot", "symbol": symbol, "sequence": sequence[symbol]}
        await websocket.send_json(snapshot | await build_book(symbol))
        while True:
            await websocket.send_json(await queue.get())
    except WebSocketDisconnect:
        pass
    finally:
        subscribers[symbol].discard(queue)
