from fastapi import FastAPI
from api.redis_routes import router as redis_router
from redis_client.config import RedisConfig
from redis_client.async_client import AsyncRedisClient
from core.dependencies import get_redis_client  # ensure import resolves in src package

app = FastAPI(title="Redis API (async)")

app.include_router(redis_router)

@app.on_event("startup")
async def startup_event():
    # create and connect client; store in app.state
    cfg = RedisConfig()  # could read env here
    app.state.redis_client = AsyncRedisClient(cfg)
    await app.state.redis_client.connect()

@app.on_event("shutdown")
async def shutdown_event():
    client = getattr(app.state, "redis_client", None)
    if client is not None:
        await client.close()
