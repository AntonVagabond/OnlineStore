import os
from functools import lru_cache
from typing import Optional, Self

from pydantic import Field, HttpUrl, PostgresDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class CommonSettings(BaseSettings):
    """Общие настройки приложения."""

    model_config = SettingsConfigDict(
        env_file=os.path.expanduser(".env"),
        env_file_encoding="utf-8",
        extra="allow",
    )


class DatabaseSettings(CommonSettings):
    """Настройки окружения базы данных."""

    pg_host: str = Field(default="localhost", alias="PG_HOST")
    pg_user: str = Field(default="postgres", alias="PG_USER")

    pg_password: str = Field(default="postgres", alias="PG_PASSWORD")
    pg_database: str = Field(default="postgres", alias="PG_DATABASE")
    pg_port: int = Field(default=5432, alias="PG_PORT")
    async_database_url: Optional[PostgresDsn] = Field(default=None)
    sync_database_url: Optional[PostgresDsn] = Field(default=None)

    @staticmethod
    def __build_db_dsn(
        username: str,
        password: str,
        host: str,
        port: int,
        database: str,
        async_dsn: bool = False,
    ) -> URL:
        """Фабрика для PostgreSQL DSN."""
        driver_name = "postgresql"
        if async_dsn:
            driver_name += "+asyncpg"
        return URL.create(
            drivername=driver_name,
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
        )

    @model_validator(mode="after")
    def validate_async_database_url(self) -> Self:
        """Построить асинхронный PostgreSQL DSN."""
        self.async_database_url = self.__build_db_dsn(
            username=self.pg_user,
            password=self.pg_password,
            host=self.pg_host,
            port=self.pg_port,
            database=self.pg_database,
            async_dsn=True,
        )
        return self

    @model_validator(mode="after")
    def validate_sync_database_url(self) -> Self:
        """Построить синхронный PostgreSQL DSN."""
        self.sync_database_url = self.__build_db_dsn(
            username=self.pg_user,
            password=self.pg_password,
            host=self.pg_host,
            port=self.pg_port,
            database=self.pg_database,
        )
        return self


class AuthSettings(CommonSettings):
    """Настройки окружения для подключения к микросервису Auth."""

    token_url: HttpUrl = Field(
        default="http://localhost:6666/api/v1/auth/login/", alias="TOKEN_URL"
    )
    auth_url: HttpUrl = Field(default="http://localhost:6666", alias="AUTH_URL")
    auth_endpoint_url: HttpUrl = Field(
        default="http://localhost:6666/api/v1/auth/authenticate/",
        alias="AUTH_ENDPOINT_URL",
    )


class HttpxSettings(CommonSettings):
    """Настройки окружения для работы с HTTP-клиентом."""

    max_connections: int = Field(default=500, alias="MAX_CONNECTIONS")
    max_keepalive_connections: int = Field(default=50, alias="MAX_KEEPALIVE_CONNECTIONS")
    keepalive_expiry: float = Field(default=30.0, alias="KEEPALIVE_EXPIRY")
    timeout: float = Field(default=20.0, alias="TIMEOUT")


class Settings(CommonSettings):
    """Настройки окружения."""

    db: DatabaseSettings = DatabaseSettings()
    auth: AuthSettings = AuthSettings()
    client: HttpxSettings = HttpxSettings()

    client_id: str = Field(default="fastapi", alias="CLIENT_ID")
    client_secret: str = Field(default="fastapi_secret", alias="CLIENT_SECRET")

    port: int = Field(default=1000, alias="PORT")
    host: str = Field(default="localhost", alias="HOST")
    page_size: int = Field(default=10, alias="PAGE_SIZE")
    openapi_url: str = Field(default="/swagger/docs/v1.0/users", alias="OPENAPI_URL")


@lru_cache
def get_settings() -> Settings:
    """
    Возвращает настройки окружения. Запрос происходит один раз, во время запуска проекта.
    """
    return Settings()


settings = get_settings()
