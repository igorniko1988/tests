"""Режим сбоев: часть запросов отвечает 503, как перегруженный сервис.

Включается переменной EXCHANGE_CHAOS_RATE (доля от 0 до 1, по умолчанию 0).
Половина сбоев случается уже после обработки запроса: изменения сохранены,
а клиент получает 503. Так в реальности выглядит ответ, потерянный по дороге.
"""

import random

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from exchange.config import settings
from exchange.errors import _body

EXEMPT_PATHS = ("/health", "/metrics", "/docs", "/redoc", "/openapi.json")


def install_chaos(app: FastAPI) -> None:
    @app.middleware("http")
    async def chaos(request: Request, call_next):
        path = request.url.path
        if settings.chaos_rate <= 0 or path == "/" or path.startswith(EXEMPT_PATHS):
            return await call_next(request)
        if random.random() >= settings.chaos_rate:
            return await call_next(request)
        if random.random() < 0.5:
            await call_next(request)
        return JSONResponse(
            status_code=503,
            content=_body("service_unavailable", "Service temporarily unavailable"),
            headers={"Retry-After": "1"},
        )
