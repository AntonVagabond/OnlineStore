from typing import Generic, TypeVar

from pydantic import Field

from common.schemas.base import BaseModel

TSchema = TypeVar("TSchema", bound=BaseModel)


class UnauthorizedResponseSchema(BaseModel, Generic[TSchema]):
    """Схема ответа при неавторизованном запросе."""
    detail: str = Field(default="Не авторизованный пользователь.")


class ForbiddenResponseSchema(BaseModel, Generic[TSchema]):
    """Схема ответа при неавторизованном запросе."""
    detail: str = Field(default="Нет прав доступа.")


class ServerErrorResponseSchema(BaseModel, Generic[TSchema]):
    """Схема ответа при неавторизованном запросе."""
    detail: str = Field(default="Ошибка сервера")
