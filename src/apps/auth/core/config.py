import os
from functools import lru_cache
from pathlib import Path
from typing import Union, Optional, Any, ClassVar

from pydantic import PostgresDsn, HttpUrl, field_validator, Field
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Настройки окружения базы данных."""
    pg_host: str = Field(alias="PG_HOST")
    pg_user: str = Field(alias="PG_USER")
    pg_password: str = Field(alias="PG_PASSWORD")
    pg_database: str = Field(alias="PG_DATABASE")
    pg_port: int = Field(alias="PG_PORT")
    async_database_uri: Union[PostgresDsn, str] = Field(
        default="", alias="ASYNC_DATABASE_URI",
    )

    model_config = SettingsConfigDict(
        env_file=os.path.expanduser(".env"),
        env_file_encoding="utf-8",
        extra="allow",
    )

    @field_validator("async_database_uri")
    def assemble_db_async_connection(
            cls, value: Optional[str], info: FieldValidationInfo,  # noqa
    ) -> Any:
        """Собственная схема для асинхронного подключения к БД."""
        if isinstance(value, str) and value == "":
            return PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=info.data["pg_user"],
                password=info.data["pg_password"],
                host=info.data["pg_host"],
                port=info.data["pg_port"],
                path=info.data["pg_database"],
            )
        return value


class AuthSettings(BaseSettings):
    """Настройки окружения для подключения к микросервису Auth."""
    token_url: HttpUrl = Field(alias="TOKEN_URL")
    private_key_path: Path = Field(alias="PRIVATE_KEY_PATH")
    public_key_path: Path = Field(alias="PUBLIC_KEY_PATH")
    algorithm: str = Field(alias="ALGORITHM")
    access_token_expire_minutes: int = Field(alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_minutes: int = Field(alias="REFRESH_TOKEN_EXPIRE_MINUTES")

    model_config = SettingsConfigDict(
        env_file=os.path.expanduser(".env"),
        env_file_encoding="utf-8",
        extra="allow",
    )


class Settings(BaseSettings):
    """Настройки окружения."""
    db: ClassVar = DatabaseSettings()
    auth: ClassVar = AuthSettings()

    client_id: str = Field(alias="CLIENT_ID")
    client_secret: str = Field(alias="CLIENT_SECRET")

    port: int = Field(alias="PORT")
    host: str = Field(alias="HOST")
    page_size: int = Field(alias="PAGE_SIZE")
    openapi_url: str = Field(alias="OPENAPI_URL")

    model_config = SettingsConfigDict(
        env_file=os.path.expanduser(".env"),
        env_file_encoding="utf-8",
        extra="allow",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Возвращает настройки окружения. Запрос происходит один раз, во время запуска проекта.
    """
    return Settings()
