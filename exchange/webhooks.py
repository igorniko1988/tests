"""Вебхуки: стенд сам шлёт POST на адрес пользователя, когда его ордер исполнен или отменён.

Тело подписано HMAC-SHA256 секретом подписки (заголовок X-Signature: sha256=<hex>).
Если приёмник не ответил 2xx, доставка повторяется с паузой 1, 2, 4 с;
у всех попыток один X-Event-Id, поэтому приёмник может отбросить дубли.
"""

import asyncio
import hashlib
import hmac
import json
import logging
import secrets
import uuid
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from fastapi import APIRouter
from sqlalchemy import select

from exchange.api.deps import Session, UserId
from exchange.config import settings
from exchange.db import Order, SessionLocal, Webhook, utcnow
from exchange.errors import ApiError
from exchange.schemas import CreateWebhookRequest, OrderOut, WebhookOut

router = APIRouter(tags=["webhooks"])
log = logging.getLogger(__name__)

# Ссылки на фоновые доставки, чтобы сборщик мусора не прервал их на середине
_deliveries: set[asyncio.Task] = set()


@router.post("/webhooks", status_code=201, response_model=WebhookOut)
async def create_webhook(body: CreateWebhookRequest, user_id: UserId, session: Session):
    webhook = Webhook(user_id=user_id, url=body.url, secret=secrets.token_hex(32))
    session.add(webhook)
    await session.commit()
    return webhook


@router.get("/webhooks", response_model=list[WebhookOut])
async def list_webhooks(user_id: UserId, session: Session):
    return list(await session.scalars(select(Webhook).where(Webhook.user_id == user_id)))


@router.delete("/webhooks/{webhook_id}", status_code=204)
async def delete_webhook(webhook_id: uuid.UUID, user_id: UserId, session: Session):
    webhook = await session.scalar(
        select(Webhook).where(Webhook.id == webhook_id, Webhook.user_id == user_id)
    )
    if webhook is None:
        raise ApiError(404, "webhook_not_found", "Webhook not found")
    await session.delete(webhook)
    await session.commit()


def sign(secret: str, body: bytes) -> str:
    return "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


def notify(order: Order, event_type: str) -> None:
    """Поставить событие в фоновую доставку; запрос, который его вызвал, не ждёт."""
    event = {
        "event_id": str(uuid.uuid4()),
        "type": event_type,
        "created_at": utcnow().isoformat(),
        "order": OrderOut.model_validate(order).model_dump(mode="json"),
    }
    _spawn(_deliver_to_user(order.user_id, event))


def _spawn(coro) -> None:
    task = asyncio.create_task(coro)
    _deliveries.add(task)
    task.add_done_callback(_deliveries.discard)


async def _deliver_to_user(user_id: uuid.UUID, event: dict) -> None:
    async with SessionLocal() as session:
        webhooks = list(await session.scalars(select(Webhook).where(Webhook.user_id == user_id)))
    for webhook in webhooks:
        _spawn(_deliver(webhook.url, webhook.secret, event))


async def _deliver(url: str, secret: str, event: dict) -> None:
    body = json.dumps(event).encode()
    headers = {
        "Content-Type": "application/json",
        "X-Event-Id": event["event_id"],
        "X-Event-Type": event["type"],
        "X-Signature": sign(secret, body),
    }
    for attempt in range(1, settings.webhook_max_attempts + 1):
        headers["X-Delivery-Attempt"] = str(attempt)
        try:
            status = await asyncio.to_thread(_post, url, body, headers)
        except OSError as error:
            status = repr(error)
        if isinstance(status, int) and 200 <= status < 300:
            return
        log.warning("webhook %s attempt %s to %s failed: %s", event["event_id"], attempt, url, status)
        if attempt < settings.webhook_max_attempts:
            await asyncio.sleep(settings.webhook_retry_delay * 2 ** (attempt - 1))


def _post(url: str, body: bytes, headers: dict) -> int:
    try:
        with urlopen(Request(url, data=body, headers=headers, method="POST"), timeout=5) as response:
            return response.status
    except HTTPError as error:
        return error.code
