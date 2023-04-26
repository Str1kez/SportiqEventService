from typing import Annotated

from fastapi import Depends
from fastapi_cache import caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend


def get_cache():
    return caches.get(CACHE_KEY)


redis_cache = Annotated[RedisCacheBackend, Depends(get_cache)]
