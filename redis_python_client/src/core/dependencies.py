from fastapi import Request, HTTPException, status

def get_redis_client(request: Request):
    """
    FastAPI dependency that returns the initialized redis client.
    Assumes main.py stored the client at app.state.redis_client.
    """
    client = getattr(request.app.state, "redis_client", None)
    if client is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Redis client not initialized")
    return client
