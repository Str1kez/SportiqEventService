import aio_pika
from aio_pika.abc import AbstractRobustConnection

from app.config.settings import DefaultSettings


settings = DefaultSettings()


# class MQManager:
#     def __init__(self) -> None:
#         self.connection: AbstractRobustConnection = None
#
#     def __new__(cls):
#         if not hasattr(cls, "instance"):
#             cls.instance = super(MQManager, cls).__new__(cls)
#         return cls.instance  # noqa
#
#     @classmethod
#     async def create(cls):
#         self = MQManager()
#         self.connection = await aio_pika.connect_robust(DefaultSettings().rabbitmq_uri)
#         return self


class MQManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, uri=settings.rabbitmq_uri):
        self.connection = None
        self.uri = uri

    async def get_connection(self) -> AbstractRobustConnection:
        if not self.connection:
            self.connection = await aio_pika.connect_robust(self.uri)
        return self.connection


# async def get_connection() -> AbstractConnection:
#     instance = await MQManager.create()
#     async with instance.connection as connection:
#         yield connection
