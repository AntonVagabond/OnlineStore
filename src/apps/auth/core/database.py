from redis import asyncio as aioredis

from .config import settings

redis_engine = aioredis.Redis(
    host=settings.redis.redis_host,
    port=settings.redis.redis_port,
    db=settings.redis.redis_db,
    password=settings.redis.redis_password,
    encoding=settings.redis.redis_encoding,
    decode_responses=settings.redis.redis_decode_responses,
    retry_on_timeout=True,
    max_connections=settings.redis.redis_pool_max_connections,
    client_name="auth_client",
    username=settings.redis.redis_user,
    ssl=settings.redis.redis_secure,
    ssl_keyfile=settings.redis.ssl_keyfile,
    ssl_certfile=settings.redis.ssl_certfile,
    ssl_cert_reqs=settings.redis.ssl_cert_reqs,
    ssl_ca_certs=settings.redis.ssl_ca_certs,
)
