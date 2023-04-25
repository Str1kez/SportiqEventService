import redis.asyncio as aioredis

from app.config.settings import DefaultSettings


class Storage:
    def __init__(self):
        self.__redis = aioredis.from_url(DefaultSettings().CACHE_URL, encoding="utf-8", decode_responses=True)

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance  # noqa

    def get_connection(self):
        return self.__redis
