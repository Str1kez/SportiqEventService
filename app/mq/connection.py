from typing import Self

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractRobustConnection
from aio_pika.pool import Pool

from app.config.settings import DefaultSettings


settings = DefaultSettings()


class MQManager:
    _instance = None

    def __new__(cls) -> Self:
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, uri=settings.rabbitmq_uri):
        self.connection = None
        self.channel_pool = None
        self.uri = uri

    async def get_connection(self) -> AbstractRobustConnection:
        if not self.connection:
            self.connection = await aio_pika.connect_robust(self.uri)
        return self.connection

    async def get_channel(self) -> AbstractChannel:
        if not self.connection:
            await self.get_connection()
        return await self.connection.channel()

    async def get_channel_pool(self) -> Pool[AbstractChannel]:
        if not self.channel_pool:
            self.channel_pool = Pool(self.get_channel, max_size=settings.MQ_CHANNEL_POOL_MAX_SIZE)
        return self.channel_pool
