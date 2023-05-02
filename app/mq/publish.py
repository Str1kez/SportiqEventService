from datetime import datetime

import aio_pika
from aio_pika.abc import AbstractChannel
from aio_pika.pool import Pool

from .type import MQEventType


async def publish_json(channel_pool: Pool[AbstractChannel], routing_key: str, body: str, type_: MQEventType) -> None:
    async with channel_pool.acquire() as channel:
        await channel.declare_queue(name=routing_key, durable=True)
        message = aio_pika.Message(
            body=body.encode(),
            content_type="application/json",
            type=type_.value,
            timestamp=datetime.utcnow(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )
        await channel.default_exchange.publish(message, routing_key=routing_key)
