import aio_pika
from aio_pika.abc import AbstractConnection, AbstractRobustConnection

from app.config.settings import DefaultSettings


class MQManager:
    def __init__(self) -> None:
        self.connection: AbstractRobustConnection = None

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(MQManager, cls).__new__(cls)
        return cls.instance  # noqa

    @classmethod
    async def create(cls):
        self = MQManager()
        self.connection = await aio_pika.connect_robust(DefaultSettings().rabbitmq_uri)
        return self


async def get_connection() -> AbstractConnection:
    instance = await MQManager.create()
    async with instance.connection as connection:
        yield connection
