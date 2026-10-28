"""Метрики Prometheus: стенд отдаёт их на GET /metrics, Prometheus забирает раз в 5 секунд (pull).

HTTP-метрики помечены шаблоном маршрута (/orders/{order_id}), а не реальным путём:
иначе каждый id ордера создал бы свой временной ряд (взрыв кардинальности).
"""

import time

from fastapi import FastAPI, Request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest
from starlette.responses import Response

SKIP_PATHS = ("/metrics", "/app", "/health", "/docs", "/redoc", "/openapi.json")

REQUESTS = Counter(
    "exchange_http_requests_total", "HTTP-запросы", ["method", "route", "status"]
)
LATENCY = Histogram(
    "exchange_http_request_duration_seconds",
    "Время ответа на HTTP-запрос",
    ["method", "route"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5),
)
IN_PROGRESS = Gauge("exchange_http_requests_in_progress", "Запросы в обработке прямо сейчас")
ORDERS_CREATED = Counter(
    "exchange_orders_created_total", "Созданные ордера", ["symbol", "side", "type"]
)
TRADES = Counter("exchange_trades_total", "Сделки (одно сопоставление BUY и SELL)", ["symbol"])
PRICE_FEED_ERRORS = Counter(
    "exchange_price_feed_errors_total", "Отказы провайдера цен", ["reason"]
)
MATCHING_DURATION = Histogram(
    "exchange_matching_cycle_seconds",
    "Длительность одного цикла сопоставления ордеров",
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1),
)


def install_metrics(app: FastAPI) -> None:
    @app.get("/metrics", include_in_schema=False)
    async def metrics() -> Response:
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    @app.middleware("http")
    async def collect(request: Request, call_next):
        if request.url.path.startswith(SKIP_PATHS):
            return await call_next(request)
        IN_PROGRESS.inc()
        start = time.perf_counter()
        status = 500
        try:
            response = await call_next(request)
            status = response.status_code
            return response
        finally:
            IN_PROGRESS.dec()
            route = request.scope.get("route")
            name = route.path if route else "unmatched"
            REQUESTS.labels(request.method, name, str(status)).inc()
            LATENCY.labels(request.method, name).observe(time.perf_counter() - start)
