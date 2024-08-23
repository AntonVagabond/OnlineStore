from typing import Optional

from httpx import AsyncClient, AsyncHTTPTransport, Limits

from core.config import settings


class HttpClient:
    """Класс инициализации/закрытия и получения клиента."""
    client: Optional[AsyncClient] = None

    @classmethod
    def start_client(cls) -> None:
        """Инициализация клиента при старте приложения."""
        transport = AsyncHTTPTransport(
            limits=Limits(
                max_connections=settings.client.max_connections,
                max_keepalive_connections=settings.client.max_keepalive_connections,
                keepalive_expiry=settings.client.keepalive_expiry,
            )
        )
        cls.client = AsyncClient(transport=transport, timeout=settings.client.timeout)

    @classmethod
    async def close_client(cls) -> None:
        """Закрытие клиента при остановке приложения."""
        await cls.client.aclose()
        cls.client = None

    @classmethod
    def get_client(cls) -> AsyncClient:
        """Получение текущего клиента."""
        if cls.client is None:
            raise RuntimeError(
                "HTTP-клиент не инициализирован. Сначала вызовите start_client."
            )
        return cls.client
