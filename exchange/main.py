import asyncio
import json
import logging
import sys
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from exchange import events, orderbook, webhooks
from exchange.api import auth, balances, orders
from exchange.chaos import install_chaos
from exchange.db import SessionLocal, create_schema
from exchange.deposits import run_deposit_consumer
from exchange.errors import install_error_handlers
from exchange.matching import run_matching


# Одна JSON-строка на запрос: по request_id запрос находится в логах (docker compose logs | grep <id>)
access_log = logging.getLogger("exchange.access")
_handler = logging.StreamHandler(sys.stdout)
_handler.setFormatter(logging.Formatter("%(message)s"))
logging.getLogger("exchange").addHandler(_handler)
logging.getLogger("exchange").setLevel(logging.INFO)
logging.getLogger("exchange").propagate = False


@asynccontextmanager
async def lifespan(_: FastAPI):
    await create_schema()
    tasks = [
        asyncio.create_task(run_matching()),
        asyncio.create_task(events.start_producer()),
        asyncio.create_task(run_deposit_consumer()),
    ]
    yield
    for task in tasks:
        task.cancel()
    await events.stop_producer()


app = FastAPI(title="Mini Exchange", version="0.1.0", lifespan=lifespan)
install_error_handlers(app)
install_chaos(app)


@app.middleware("http")
async def request_id(request: Request, call_next):
    rid = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    start = time.perf_counter()
    entry = {"level": "INFO", "request_id": rid, "method": request.method, "path": request.url.path}
    try:
        response = await call_next(request)
    except Exception as error:
        entry |= {"level": "ERROR", "status": 500, "error": repr(error)}
        raise
    else:
        entry["status"] = response.status_code
        if response.status_code >= 500:
            entry["level"] = "ERROR"
        elif response.status_code >= 400:
            entry["level"] = "WARNING"
        response.headers["X-Request-ID"] = rid
        return response
    finally:
        entry["duration_ms"] = round((time.perf_counter() - start) * 1000, 1)
        if not request.url.path.startswith("/app"):
            access_log.info(json.dumps(entry))


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/app/")


@app.get("/health", tags=["system"])
async def health():
    async with SessionLocal() as session:
        await session.execute(text("SELECT 1"))
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(balances.router)
app.include_router(orders.router)
app.include_router(orderbook.router)
app.include_router(webhooks.router)

app.mount("/app", StaticFiles(directory=Path(__file__).parent / "web", html=True), name="web")
