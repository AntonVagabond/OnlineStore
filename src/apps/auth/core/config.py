import os
from functools import lru_cache
from pathlib import Path

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Optional


class CommonSettings(BaseSettings):
    """Общие настройки."""

    model_config = SettingsConfigDict(
        env_file=os.path.expanduser(".env"),
        env_file_encoding="utf-8",
        extra="allow",
    )


class AuthSettings(CommonSettings):
    """Настройки окружения для подключения к микросервису Auth."""

    token_url: HttpUrl = Field(
        default="http://localhost:1500/api/v1/auth/login/", alias="TOKEN_URL"
    )
    user_endpoint_url: HttpUrl = Field(
        default="http://localhost:1000/api/v1/users/get_user_for_auth/",
        alias="USER_ENDPOINT_URL",
    )

    private_key_path: Path = Field(
        default="certs/jwt-private.pem", alias="PRIVATE_KEY_PATH"
    )
    public_key_path: Path = Field(default="certs/jwt-public.pem", alias="PUBLIC_KEY_PATH")
    algorithm: str = Field(default="RS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=5, alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    refresh_token_expire_minutes: int = Field(
        default=10, alias="REFRESH_TOKEN_EXPIRE_MINUTES"
    )


class RedisSettings(CommonSettings):
    """Настройки окружения для Redis."""

    redis_secure: bool = Field(default=True, alias="REDIS_SECURE")
    redis_host: str = Field(default="0.0.0.0", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")
    redis_user: str = Field(default="default", alias="REDIS_USER")
    redis_password: str = Field(default="redis", alias="REDIS_PASSWORD")
    redis_db: int = Field(default=0, alias="REDIS_DB")
    redis_decode_responses: bool = Field(default=True, alias="REDIS_DECODE_RESPONSES")
    redis_encoding: str = Field(default="utf-8", alias="REDIS_ENCODING")
    redis_pool_max_connections: int = Field(
        default=100, alias="REDIS_POOL_MAX_CONNECTIONS"
    )
    ssl_keyfile: Optional[str] = Field(default=None, alias="SSL_KEYFILE")
    ssl_certfile: Optional[str] = Field(default=None, alias="SSL_CERTFILE")
    ssl_cert_reqs: Optional[str] = Field(default=None, alias="SSL_CERT_REQS")
    ssl_ca_certs: Optional[str] = Field(default=None, alias="SSL_CA_CERTS")


class HttpxSettings(CommonSettings):
    """Настройки окружения для работы с HTTP-клиентом."""

    max_connections: int = Field(default=500, alias="MAX_CONNECTIONS")
    max_keepalive_connections: int = Field(default=50, alias="MAX_KEEPALIVE_CONNECTIONS")
    keepalive_expiry: float = Field(default=30.0, alias="KEEPALIVE_EXPIRY")
    timeout: float = Field(default=20.0, alias="TIMEOUT")


class Settings(CommonSettings):
    """Настройки окружения."""

    auth: AuthSettings = AuthSettings()
    redis: RedisSettings = RedisSettings()
    client: HttpxSettings = HttpxSettings()

    client_id: str = Field(default="fastapi", alias="CLIENT_ID")
    client_secret: str = Field(default="fastapi_secret", alias="CLIENT_SECRET")

    port: int = Field(default=1500, alias="PORT")
    host: str = Field(default="localhost", alias="HOST")
    page_size: int = Field(default=10, alias="PAGE_SIZE")
    openapi_url: str = Field(default="/swagger/docs/v1.0/auth", alias="OPENAPI_URL")


@lru_cache
def get_settings() -> Settings:
    """
    Возвращает настройки окружения. Запрос происходит один раз, во время запуска проекта.
    """
    return Settings()


settings = get_settings()
