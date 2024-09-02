import json
from typing import Optional, Callable, Coroutine, Any
from uuid import UUID

import httpx
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from httpx import AsyncClient

from common.schemas.api.mixins import CurrentUserSchema
from core.config import settings
from core.http_connector import ExternalServiceConnector

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=str(settings.auth.token_url), scheme_name="JWT",
)


def get_current_user(
        roles: Optional[tuple[str, ...]] = None,
) -> Callable[[AsyncClient, str], Coroutine[Any, Any, CurrentUserSchema]]:
    """Возвращает авторизованного пользователя."""

    async def current_user(
            client: AsyncClient = Depends(ExternalServiceConnector.get_client),
            token: str = Depends(oauth2_scheme),
    ) -> CurrentUserSchema:
        """Поиск текущего пользователя."""
        data = {
            "access_token": token,
            "roles": ', '.join(roles) if roles else None
        }
        filter_data = {key: value for key, value in data.items() if value is not None}

        try:
            response = await client.get(
                url=str(settings.auth.auth_endpoint_url), headers=filter_data,
            )
            response.raise_for_status()  # Проверка на HTTP ошибки.
            response_json = response.json()  # Конвертируем ответ в json-формат.
        except httpx.HTTPStatusError as error:
            raise HTTPException(
                status_code=error.response.status_code,
                detail=json.loads(error.response.text)["detail"],
                headers=error.response.headers,
            )
        except httpx.RequestError as error:
            raise HTTPException(
                status_code=500,
                detail=f"Request failed: {error}",
            )

        return CurrentUserSchema(id=UUID(response_json["id"]))

    return current_user
