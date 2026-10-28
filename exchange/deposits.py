"""Депозиты из RabbitMQ: платёжный сервис кладёт сообщение в очередь deposits, стенд зачисляет.

Тело: {"user_id": "<uuid>", "asset": "USDT", "amount": "100"}, свойство message_id обязательно.
Повтор с тем же message_id подтверждается, но второй раз не зачисляется.
Битое сообщение (не JSON, неверные поля, нет message_id, нет пользователя) уходит в deposits.dlq.
Без EXCHANGE_RABBITMQ_URL выключено.
"""

import asyncio
import logging

import aio_pika
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from exchange.api.balances import lock_balance
from exchange.config import settings
from exchange.db import ProcessedMessage, SessionLocal, User
from exchange.schemas import DepositMessage

QUEUE = "deposits"
DEAD_LETTER_QUEUE = "deposits.dlq"
log = logging.getLogger(__name__)


class BadMessage(Exception):
    pass


async def run_deposit_consumer() -> None:
    if not settings.rabbitmq_url:
        return
    while True:
        try:
            connection = await aio_pika.connect_robust(settings.rabbitmq_url)
            break
        except Exception as error:
            log.warning("rabbitmq is not ready: %r", error)
            await asyncio.sleep(2)
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        await channel.declare_queue(DEAD_LETTER_QUEUE, durable=True)
        queue = await channel.declare_queue(
            QUEUE,
            durable=True,
            arguments={"x-dead-letter-exchange": "", "x-dead-letter-routing-key": DEAD_LETTER_QUEUE},
        )
        log.info("consuming %s", QUEUE)
        async with queue.iterator() as messages:
            async for message in messages:
                await handle(message)


async def handle(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    try:
        await _credit(message)
    except BadMessage as error:
        log.warning("deposit message %s rejected: %s", message.message_id, error)
        await message.reject(requeue=False)
    else:
        await message.ack()


async def _credit(message) -> None:
    if not message.message_id:
        raise BadMessage("message_id is required")
    try:
        deposit = DepositMessage.model_validate_json(message.body)
    except ValidationError as error:
        raise BadMessage(str(error)) from None

    async with SessionLocal() as session:
        if await session.get(User, deposit.user_id) is None:
            raise BadMessage("unknown user")
        session.add(ProcessedMessage(message_id=message.message_id))
        try:
            await session.flush()
        except IntegrityError:
            log.info("deposit message %s already processed", message.message_id)
            return
        balance = await lock_balance(session, deposit.user_id, deposit.asset)
        balance.available += deposit.amount
        await session.commit()
