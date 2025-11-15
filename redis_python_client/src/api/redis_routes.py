from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

router = APIRouter(prefix="/redis", tags=["Redis"])

def get_client(request: Request):
    client = request.app.state.redis_client
    if not client:
        raise HTTPException(status_code=500, detail="Redis client not initialized")
    return client

@router.post("/set")
async def set_key(request: Request, payload: dict):
    client = get_client(request)
    success = await client.set(
        payload["key"],
        payload["value"],
        ex=payload.get("expire")
    )
    return {"message": "Chave criada com sucesso!" if success else "FAIL"}


@router.get("/get/{key}")
async def get_key(request: Request, key: str):
    client = get_client(request)
    value = await client.get(key)
    return {"value": value}


@router.delete("/delete/{key}")
async def delete_key(key: str, request: Request):
    client = get_client(request)
    return await client.delete(key)

@router.get("/exists/{key}")
async def exists_key(key: str, request: Request):
    client = get_client(request)
    return await client.exists(key)

@router.get("/ttl/{key}")
async def ttl_key(key: str, request: Request):
    client = get_client(request)
    return await client.ttl(key)

@router.post("/incr")
async def incr_key(payload: dict, request: Request):
    client = get_client(request)
    return await client._client.incr(payload["key"])

@router.post("/expire")
async def expire_key(payload: dict, request: Request):
    client = get_client(request)
    return await client._client.expire(payload["key"], payload["seconds"])
