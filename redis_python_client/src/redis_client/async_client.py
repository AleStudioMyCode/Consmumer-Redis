from __future__ import annotations
from typing import Any, Optional, Dict
import redis.asyncio as aioredis
from .config import RedisConfig
from .exceptions import RedisConnectionError, RedisClientError
from .utils import get_logger

logger = get_logger(__name__)

class AsyncRedisClient:
    def __init__(self, config: Optional[RedisConfig] = None):
        self._config = config or RedisConfig()
        self._client: Optional[aioredis.Redis] = None

    async def connect(self) -> None:
        if self._client is not None:
            return
        try:
            self._client = aioredis.from_url(
                f"redis://{self._config.host}:{self._config.port}/{self._config.db}",
                password=self._config.password,
                decode_responses=self._config.decode_responses,
            )
            await self._client.ping()
            logger.info("Connected to Redis (async)")
        except Exception as exc:
            logger.exception("Async connect failed")
            raise RedisConnectionError("Failed to connect to Redis") from exc

    async def close(self) -> None:
        if self._client:
            try:
                await self._client.close()
            except Exception:
                pass
            self._client = None
            logger.info("Redis connection closed (async)")

    # key-value
    async def set(self, key: str, value: Any, ex: Optional[int] = None):
        if self._client is None:
            await self.connect()
        return await self._client.set(key, value, ex=ex)

    async def get(self, key: str):
        if self._client is None:
            await self.connect()
        return await self._client.get(key)

    async def delete(self, *keys: str) -> int:
        if self._client is None:
            await self.connect()
        return await self._client.delete(*keys)

    async def exists(self, key: str) -> int:
        if self._client is None:
            await self.connect()
        return await self._client.exists(key)

    async def ttl(self, key: str) -> int:
        if self._client is None:
            await self.connect()
        return await self._client.ttl(key)

    # pub/sub simple publish (non-blocking)
    async def publish(self, channel: str, message: str) -> int:
        if self._client is None:
            await self.connect()
        return await self._client.publish(channel, message)
