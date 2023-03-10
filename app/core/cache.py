from dataclasses import dataclass

import aioredis
from aioredis import Redis


@dataclass
class Cache:
    """
    class to handle tha cache connection
    """

    def __init__(self, cache_host: str, cache_password: str):
        # redis connection
        self._redis: Redis = aioredis.from_url(
            cache_host,
            encoding="utf-8",
            decode_responses=True,
            password=cache_password
        )
