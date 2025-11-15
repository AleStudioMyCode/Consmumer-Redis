from dataclasses import dataclass
from typing import Optional


@dataclass
class RedisConfig:
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    max_connections: int = 10
    decode_responses: bool = True
    socket_timeout: Optional[float] = 5.0

