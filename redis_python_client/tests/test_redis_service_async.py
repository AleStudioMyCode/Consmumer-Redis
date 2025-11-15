import pytest
import fakeredis
from redis_client.async_client import AsyncRedisClient
from redis_client.config import RedisConfig
from services.redis_service import set_key, get_key, delete_key

# async fake wrapper
class AsyncFakeRedis:
    def __init__(self, fake):
        self._fake = fake
    async def set(self, *args, **kwargs):
        return self._fake.set(*args, **kwargs)
    async def get(self, *args, **kwargs):
        return self._fake.get(*args, **kwargs)
    async def delete(self, *args, **kwargs):
        return self._fake.delete(*args, **kwargs)
    async def exists(self, *args, **kwargs):
        return self._fake.exists(*args, **kwargs)
    async def ttl(self, *args, **kwargs):
        return self._fake.ttl(*args, **kwargs)
    async def publish(self, *args, **kwargs):
        return self._fake.publish(*args, **kwargs)
    async def ping(self):
        return True
    async def close(self):
        return None

@pytest.mark.asyncio
async def test_service_set_get_delete(monkeypatch):
    server = fakeredis.FakeServer()
    fake = fakeredis.FakeRedis(server=server, decode_responses=True)
    async_fake = AsyncFakeRedis(fake)

    async def _fake_connect(self):
        self._client = async_fake

    monkeypatch.setattr(AsyncRedisClient, "connect", _fake_connect)

    client = AsyncRedisClient(RedisConfig())
    await client.connect()
    await set_key(client, "k1", "v1", ex=5)
    val = await get_key(client, "k1")
    assert val == "v1"
    await delete_key(client, "k1")
    assert await get_key(client, "k1") is None
