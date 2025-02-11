from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import EmailStr, field_validator

from common.schemas.api.mixins import RegisterSchema, UpdateSchema
from common.schemas.base import BaseModel


class ProfileResponseSchema(BaseModel):
    """Схема ответа на запрос профиля."""

    id: UUID
    last_name: str
    first_name: str
    second_name: str
    phone_number: str
    email: EmailStr
    is_man: bool
    photo: Optional[str]
    birthday: datetime

    @field_validator("birthday")
    def validate_birthday(cls, birthday: datetime) -> datetime:  # noqa
        """Преобразование даты рождения под нужный формат."""
        datetime_str = birthday.strftime("%Y-%m-%d %H:%M:%S")
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")


class RegisterUserSchema(RegisterSchema):
    """Схема для регистрации пользователя."""


class UpdateUserSchema(UpdateSchema):
    """Схема для обновления пользователя."""


class UserForAuthResponseSchema(BaseModel):
    """Базовая схема человека для авторизации."""

    id: UUID
    email: EmailStr
    role_name: Optional[str]
    hash_password: bytes
    deleted: bool
