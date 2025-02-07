import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class PostgresConfig:
    """Класс конфигурации для PostgreSQL."""

    user: str = os.getenv("PG_USER", "postgres")
    password: str = os.getenv("PG_PASSWORD", "postgres")
    host: str = os.getenv("PG_HOST", "localhost")
    port: int = int(os.getenv("PG_PORT", 5432))
    database: str = os.getenv("PG_DATABASE", "postgres")
    echo: bool = field(default=False)

    @property
    def postgres_dsn(self) -> str:
        """Возвращает DSN для подключения к PostgreSQL."""
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}"
        )
