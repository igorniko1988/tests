import asyncio
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import text

from exchange import orderbook
from exchange.api import auth, balances, orders
from exchange.chaos import install_chaos
from exchange.db import SessionLocal, create_schema
from exchange.errors import install_error_handlers
from exchange.matching import run_matching


@asynccontextmanager
async def lifespan(_: FastAPI):
    await create_schema()
    matching = asyncio.create_task(run_matching())
    yield
    matching.cancel()


app = FastAPI(title="Mini Exchange", version="0.1.0", lifespan=lifespan)
install_error_handlers(app)
install_chaos(app)


@app.middleware("http")
async def request_id(request: Request, call_next):
    rid = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = rid
    return response


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")


@app.get("/health", tags=["system"])
async def health():
    async with SessionLocal() as session:
        await session.execute(text("SELECT 1"))
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(balances.router)
app.include_router(orders.router)
app.include_router(orderbook.router)
