from __future__ import annotations
from typing import Any, Dict, Optional, List
import time
import redis

from .config import RedisConfig
from .exceptions import RedisClientError, RedisConnectionError
from .utils import get_logger

logger = get_logger(__name__)

class RedisClient:
    def __init__(self, config: Optional[RedisConfig] = None, retry: int = 3, retry_backoff: float = 0.3):
        self._config = config or RedisConfig()
        self._retry = int(retry)
        self._retry_backoff = float(retry_backoff)
        self._pool: Optional[redis.ConnectionPool] = None
        self._client: Optional[redis.Redis] = None
        self._connect()

    def _connect(self) -> None:
        try:
            self._pool = redis.ConnectionPool(
                host=self._config.host,
                port=self._config.port,
                db=self._config.db,
                password=self._config.password,
                max_connections=self._config.max_connections,
                decode_responses=self._config.decode_responses,
                socket_timeout=self._config.socket_timeout,
            )
            self._client = redis.Redis(connection_pool=self._pool)
            self._client.ping()
        except Exception as exc:
            logger.exception("Falha ao conectar no Redis")
            raise RedisConnectionError("Não foi possível conectar ao Redis") from exc

    def _with_retries(self, func, *args, **kwargs):
        last_exc = None
        for attempt in range(1, self._retry + 1):
            try:
                if self._client is None:
                    self._connect()
                return func(*args, **kwargs)
            except Exception as exc:
                last_exc = exc
                logger.warning("Tentativa %s falhou: %s", attempt, exc)
                time.sleep(self._retry_backoff * attempt)
                try:
                    self._connect()
                except Exception:
                    pass
        logger.exception("Todas as tentativas falharam")
        raise RedisClientError("Operação falhou após tentativas") from last_exc

    def __enter__(self) -> "RedisClient":
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False

    def close(self) -> None:
        if self._pool:
            try:
                self._pool.disconnect()
            except Exception:
                pass

    # Key-value
    def set(self, key: str, value: Any, ex: Optional[int] = None, px: Optional[int] = None, nx: bool = False, xx: bool = False) -> bool:
        return self._with_retries(self._client.set, key, value, ex=ex, px=px, nx=nx, xx=xx)

    def get(self, key: str) -> Optional[Any]:
        return self._with_retries(self._client.get, key)

    def delete(self, *keys: str) -> int:
        return self._with_retries(self._client.delete, *keys)

    def exists(self, key: str) -> int:
        return self._with_retries(self._client.exists, key)

    def expire(self, key: str, seconds: int) -> bool:
        return self._with_retries(self._client.expire, key, seconds)

    def ttl(self, key: str) -> int:
        return self._with_retries(self._client.ttl, key)
