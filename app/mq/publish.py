from datetime import datetime

import aio_pika
from aio_pika.abc import AbstractConnection

from .type import MQMessageType


async def publish_json(connection: AbstractConnection, routing_key: str, body: str, type_: MQMessageType):
    channel = await connection.channel()
    await channel.declare_queue(name=routing_key, durable=True)
    message = aio_pika.Message(
        body=body.encode(),
        type=type_.value,
        timestamp=datetime.utcnow(),
        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
    )
    await channel.default_exchange.publish(message, routing_key=routing_key)
