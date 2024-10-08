import uuid

from pydantic import Field

from common.const import response_exceptions as resp_exc
from common.schemas.base import BaseModel


class SuccessIdResponseSchema(BaseModel):
    """Схема ответа при успешном регистрации пользователя."""

    detail: str = Field(default=uuid.uuid4())


class SuccessBoolResponseSchema(BaseModel):
    """Схема ответа при успешном выполнении операции."""

    detail: bool = Field(default=True)


class BadRequestResponseSchema(BaseModel):
    """Схема ответа при неправильном запросе."""

    detail: str = Field(default="Некорректные данные.")


class UnauthorizedResponseSchema(BaseModel):
    """Схема ответа при неавторизованном запросе."""

    detail: str = Field(default="Не авторизованный пользователь.")


class ForbiddenResponseSchema(BaseModel):
    """Схема ответа при запрете на конечную точку."""

    detail: str = Field(default="Нет прав доступа.")


class ForbiddenAdminResponseSchema(BaseModel):
    """Схема ответа при запрете на конечную точку с ролью admin."""

    detail: str = Field(default="Для этого действия требуется роль: 'admin'.")


class NotFoundResponseSchema(BaseModel):
    """Схема ответа при не найденном ресурсе."""

    detail: str = Field(default="Данные не найдены.")


class UserNotFoundResponseSchema(BaseModel):
    """Схема ответа при не найденном ресурсе."""

    detail: str = Field(default=resp_exc.USER_NOT_FOUND)


class ServerErrorResponseSchema(BaseModel):
    """Схема ответа при неавторизованном запросе."""

    detail: str = Field(default="Ошибка сервера")
