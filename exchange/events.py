"""События ордеров в Kafka: топик orders.events, ключ сообщения — id ордера.

Типы: order.created, order.partially_filled, order.filled, order.canceled.
Ключ = id ордера, поэтому все события одного ордера попадают в одну партицию
и читаются в том порядке, в каком отправлены. Партиций 3: порядок между
разными ордерами не гарантирован. Без EXCHANGE_KAFKA_BOOTSTRAP выключено.
"""

import asyncio
import json
import logging
import uuid

from aiokafka import AIOKafkaProducer
from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from aiokafka.errors import TopicAlreadyExistsError

from exchange.config import settings
from exchange.db import Order, utcnow
from exchange.schemas import OrderOut

TOPIC = "orders.events"
PARTITIONS = 3
log = logging.getLogger(__name__)
_producer: AIOKafkaProducer | None = None


async def start_producer() -> None:
    """Подключается к брокеру в фоне: брокер может подняться позже стенда."""
    global _producer
    if not settings.kafka_bootstrap:
        return
    while True:
        producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_bootstrap, acks="all")
        try:
            await producer.start()
        except Exception as error:
            log.warning("kafka is not ready: %r", error)
            await producer.stop()
            await asyncio.sleep(2)
            continue
        await _create_topic()
        _producer = producer
        log.info("kafka producer connected to %s", settings.kafka_bootstrap)
        return


async def _create_topic() -> None:
    admin = AIOKafkaAdminClient(bootstrap_servers=settings.kafka_bootstrap)
    await admin.start()
    try:
        await admin.create_topics([NewTopic(TOPIC, num_partitions=PARTITIONS, replication_factor=1)])
    except TopicAlreadyExistsError:
        pass
    finally:
        await admin.close()


async def stop_producer() -> None:
    if _producer is not None:
        await _producer.stop()


def build_event(order: Order, event_type: str) -> dict:
    """Снимок ордера на момент события: в сделке ордер меняется несколько раз подряд."""
    return {
        "event_id": str(uuid.uuid4()),
        "type": event_type,
        "created_at": utcnow().isoformat(),
        "order": OrderOut.model_validate(order).model_dump(mode="json"),
    }


async def send(event: dict) -> None:
    if _producer is None:
        return
    try:
        await _producer.send_and_wait(
            TOPIC,
            key=event["order"]["id"].encode(),
            value=json.dumps(event).encode(),
            headers=[("event_type", event["type"].encode())],
        )
    except Exception:
        log.exception("failed to publish %s", event["type"])
