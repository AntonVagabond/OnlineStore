from typing import Optional

from pydantic import Field

from common.schemas.base import BaseModel


class TokenInfoSchema(BaseModel):
    """Схема информации о токене."""

    access_token: str
    token_type: str = Field(default="Bearer")


class LogoutResponseSchema(BaseModel):
    """Ответ при выходе из учетной записи."""

    message: str = Field(default="Вы успешно вышли из учетной записи.")


class EmptyUserSchema(BaseModel):
    """Пустой пользователь."""


class UserInfoSchema(BaseModel):
    """Схема информации о пользователе."""

    id: str
    email: str
    deleted: bool
    role_name: Optional[str]
