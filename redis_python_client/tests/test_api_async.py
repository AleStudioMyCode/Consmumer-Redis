# tests/test_api_async.py

import pytest
from httpx import AsyncClient, ASGITransport
import fakeredis
from redis_client.async_client import AsyncRedisClient
from main import app


class AsyncFakeRedis:
    def __init__(self, sync_client):
        self._sync = sync_client

    async def get(self, key):
        return self._sync.get(key)

    async def set(self, key, value, ex=None, **kwargs):
        # fakeredis usa argumento expire ao invés de ex
        if ex is not None:
            return self._sync.set(key, value, ex=ex)
        return self._sync.set(key, value)

    async def delete(self, key):
        return self._sync.delete(key)

    async def exists(self, key):
        return self._sync.exists(key)

    async def ttl(self, key):
        return self._sync.ttl(key)

    async def publish(self, channel, message):
        return self._sync.publish(channel, message)


@pytest.fixture
async def app_client(monkeypatch):

    server = fakeredis.FakeServer()
    fake_sync = fakeredis.FakeRedis(server=server, decode_responses=True)
    fake_async = AsyncFakeRedis(fake_sync)

    async def _fake_connect(self):
        self._client = fake_async

    monkeypatch.setattr(AsyncRedisClient, "connect", _fake_connect)

    transport = ASGITransport(app=app)

    # 🔥 Força o FastAPI a rodar startup()
    await app.router.startup()

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    # 🔥 Força o FastAPI a rodar shutdown()
    await app.router.shutdown()



# -----------------------
# TEST REAL
# -----------------------
async def test_api_set_get(app_client):

    # SET
    response = await app_client.post("/redis/set", json={"key": "x", "value": "123"})
    assert response.status_code == 200
    assert response.json()["message"] == "Chave criada com sucesso!"

    # GET
    response = await app_client.get("/redis/get/x")
    assert response.status_code == 200
    assert response.json()["value"] == "123"
