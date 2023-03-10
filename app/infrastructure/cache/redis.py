"""
core configuration for redis connection
"""
import json
import logging
from dataclasses import dataclass

import aioredis
from aioredis import Redis

logger = logging.getLogger(__name__)


@dataclass
class CacheClient:
    """
    class to represent the redis connection
    """

    redis: Redis
    cache_default_ttl: int

    @classmethod
    def cache_prefix(cls, value: str) -> str:
        """
        generate cache prefix with and value
        """
        return f"SELLER_ID:{value}"

    async def set_cache(self, key: str, data: dict) -> None:
        """
        async function set redis key value pais
        """
        try:
            await self.redis.set(key, json.dumps(data), ex=self.cache_default_ttl)
        except aioredis.exceptions.ConnectionError as error:
            logger.error(error)

    async def get_cache(self, key: str) -> dict:
        """
        async function get redis key value
        """
        return json.loads(await self.redis.get(key))

    async def cache_exists(self, key: str) -> int:
        """
        async function to check if key exists
        """
        try:
            return await self.redis.exists(key)
        except aioredis.exceptions.ConnectionError as error:
            logger.error(error)
            return 0
