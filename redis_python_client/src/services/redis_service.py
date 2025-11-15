from typing import Any, Optional
from redis_client.async_client import AsyncRedisClient

# service functions that operate using an AsyncRedisClient instance

async def set_key(client: AsyncRedisClient, key: str, value: Any, ex: Optional[int] = None):
    return await client.set(key, value, ex=ex)

async def get_key(client: AsyncRedisClient, key: str):
    return await client.get(key)

async def delete_key(client: AsyncRedisClient, key: str):
    return await client.delete(key)

async def exists_key(client: AsyncRedisClient, key: str):
    return await client.exists(key)

async def ttl_key(client: AsyncRedisClient, key: str):
    return await client.ttl(key)

async def publish_message(client: AsyncRedisClient, channel: str, message: str):
    return await client.publish(channel, message)
