from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import EmailStr, field_validator, ValidationError, Field

from common.schemas.api.mixins import RegisterSchema
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


class UpdateUserSchema(BaseModel):
    """Схема для обновления пользователя."""
    last_name: str
    first_name: str
    second_name: str
    birthday: Optional[datetime] = Field(default=None)
    phone_number: str
    date_update: datetime = Field(
        default=datetime.now(), json_schema_extra={"hidden": True},
    )

    @field_validator("last_name")
    def validate_last_name(cls, last_name: str) -> str:  # noqa
        """Проверка отчества."""
        if 2 <= len(last_name) <= 50:
            return last_name
        raise ValidationError("Символов в отчестве должно быть больше 1 либо меньше 51.")

    @field_validator("first_name")
    def validate_first_name(cls, first_name: str) -> str:  # noqa
        """Проверка имени."""
        if 2 <= len(first_name) <= 50:
            return first_name
        raise ValidationError("Символов в имени должно быть больше 1 либо меньше 51.")

    @field_validator("second_name")
    def validate_second_name(cls, second_name: str) -> str:  # noqa
        """Проверка фамилии."""
        if 2 <= len(second_name) <= 50:
            return second_name
        raise ValidationError("Символов в фамилии должно быть больше 1 либо меньше 51.")

    @field_validator("birthday")
    def validate_birthday(cls, birthday: datetime) -> datetime:  # noqa
        """Преобразование даты рождения под нужный формат."""
        datetime_str = birthday.strftime("%Y-%m-%d %H:%M:%S")
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
