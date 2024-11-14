import httpx
from typing_extensions import Optional

from core.http_connector import ExternalServiceConnector


class UserClientService:
    """Клиент микросервиса Users."""

    def __init__(self, url: str) -> None:
        self.url = url
        self.__client = ExternalServiceConnector.get_client()

    async def get_user_over_httpx(
        self,
        username: str,
    ) -> Optional[dict[str, ...]]:
        """Получить пользователя, если он есть на микросервисе Users через httpx."""
        try:
            response = await self.__client.get(
                url=self.url, headers={"username": username}
            )
            response.raise_for_status()  # Проверка на HTTP ошибки.
            response_json = response.json()  # Конвертируем ответ в json-формат.
        except (httpx.HTTPStatusError, httpx.RequestError):
            return None
        return response_json
