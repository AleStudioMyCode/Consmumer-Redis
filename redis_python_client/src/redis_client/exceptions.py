class RedisClientError(Exception):
    """Base Redis client error."""
    pass

class RedisConnectionError(RedisClientError):
    """Raised when connection to Redis fails."""
    pass
