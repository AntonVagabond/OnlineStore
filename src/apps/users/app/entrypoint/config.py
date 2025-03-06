import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class AppConfig:
    """Класс конфигурации приложения."""

    openapi_url: str = os.getenv("OPENAPI_URL", "/swagger/docs/v1.0/users")
    client_id: str = os.getenv("CLIENT_ID", "fastapi")
    client_secret: str = os.getenv("CLIENT_SECRET", "fastapi_secret")
    page_size: int = int(os.getenv("PAGE_SIZE", 10))
