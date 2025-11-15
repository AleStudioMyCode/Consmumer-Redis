from src.redis_client.client import RedisClient
from src.redis_client import RedisConfig

config = RedisConfig()

client = RedisClient(config)


print("SET:", client.set("teste:sync", "funcionando!", ex=100))
print("GET:", client.get("teste:sync"))
print("EXISTS:", client.exists("teste:sync"))
print("TTL:", client.ttl("teste:sync"))
