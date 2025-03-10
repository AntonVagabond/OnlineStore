import os
from dataclasses import dataclass
from typing import Self

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class PostgresConfig:
    """Класс конфигурации для PostgreSQL."""

    host: str
    port: int
    user: str
    password: str
    db: str

    uri: str

    @classmethod
    def from_env(cls) -> Self:
        """Возвращает настройки PostgreSQL."""

        host = os.getenv("PG_HOST", "localhost")
        port = int(os.getenv("PG_PORT", 5432))
        user = os.getenv("PG_USER", "postgres")
        password = os.getenv("PG_PASSWORD", "postgres")
        db = os.getenv("PG_DATABASE", "postgres")

        uri = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"

        return cls(host=host, port=port, user=user, password=password, db=db, uri=uri)
