"""Внешний провайдер цен: MARKET-ордер берёт цену отсюда.

GET {EXCHANGE_PRICE_FEED_URL}/prices/{symbol} → {"symbol", "price", "timestamp"}.
Ошибка, таймаут или цена старше EXCHANGE_PRICE_MAX_AGE секунд — ордер не создаётся (503).
"""

import asyncio
import json
from datetime import UTC, datetime, timedelta
from decimal import Decimal, InvalidOperation
from urllib.request import urlopen

from exchange.config import settings
from exchange.errors import ApiError
from exchange.metrics import PRICE_FEED_ERRORS


def _fetch(url: str, timeout: float) -> dict:
    with urlopen(url, timeout=timeout) as response:
        return json.load(response)


async def current_price(symbol: str) -> Decimal:
    if not settings.price_feed_url:
        raise ApiError(503, "price_unavailable", "Price feed is not configured")
    url = f"{settings.price_feed_url.rstrip('/')}/prices/{symbol}"
    try:
        data = await asyncio.to_thread(_fetch, url, settings.price_feed_timeout)
        price = Decimal(str(data["price"]))
        timestamp = datetime.fromisoformat(data["timestamp"])
    except (OSError, ValueError, KeyError, TypeError, InvalidOperation):
        # OSError покрывает HTTPError (не 2xx), обрыв соединения и таймаут
        PRICE_FEED_ERRORS.labels("unavailable").inc()
        raise ApiError(503, "price_unavailable", "Price feed is unavailable") from None
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=UTC)
    if datetime.now(UTC) - timestamp > timedelta(seconds=settings.price_max_age):
        PRICE_FEED_ERRORS.labels("stale").inc()
        raise ApiError(503, "price_stale", "Price feed returned a stale price")
    return price
