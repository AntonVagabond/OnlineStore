from pydantic import Field

from common.schemas.base import BaseModel


class BadRequestResponseSchema(BaseModel):
    """Схема ответа при неправильном запросе."""
    detail: str = Field(default="Некорректные данные.")


class UnauthorizedResponseSchema(BaseModel):
    """Схема ответа при неавторизованном запросе."""
    detail: str = Field(default="Не авторизованный пользователь.")


class ForbiddenResponseSchema(BaseModel):
    """Схема ответа при неавторизованном запросе."""
    detail: str = Field(default="Нет прав доступа.")


class NotFoundResponseSchema(BaseModel):
    """Схема ответа при не найденном ресурсе."""
    detail: str = Field(default="Данные не найдены.")


class ServerErrorResponseSchema(BaseModel):
    """Схема ответа при неавторизованном запросе."""
    detail: str = Field(default="Ошибка сервера")
