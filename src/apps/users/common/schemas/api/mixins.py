from datetime import datetime
from typing import TypeVar, Optional
from uuid import UUID

from pydantic import Field, EmailStr, field_validator, ValidationError

from common.enums.role import Role
from common.schemas.base import BaseModel

TSchema = TypeVar("TSchema", bound=BaseModel)


class CurrentUserSchema(BaseModel):
    """Схема текущего пользователя."""
    id: UUID


class PersonBaseSchema(BaseModel):
    """Базовая схема человека."""
    id: UUID
    email: EmailStr
    phone_number: Optional[str] = Field(default=None)
    photo: Optional[bytes] = Field(default=None)
    full_name: Optional[str] = Field(default=None)


class PersonSchema(PersonBaseSchema):
    """Схема человека."""
    last_name: Optional[str] = Field(default=None)
    first_name: Optional[str] = Field(default=None)
    second_name: Optional[str] = Field(default=None)
    role: str
    is_man: bool = Field(default=True)
    birthday: Optional[datetime] = Field(default=None)


class StandardViewSchemaForTable(PersonSchema):
    """Схема стандартного представления для таблицы."""


class RegisterSchema(BaseModel):
    """Общая схема для регистрации."""
    role: Role
    email: EmailStr
    phone_number: str
    password_hash: str
    last_name: str
    first_name: str
    second_name: str
    is_man: bool = Field(default=True)
    birthday: Optional[datetime] = Field(default=None)
    date_add: datetime = Field(default=datetime.now(), hidden=True)  # type: ignore
    date_update: datetime = Field(default=datetime.now(), hidden=True)  # type: ignore

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

    @field_validator("password_hash")
    def validate_password(cls, password: str) -> str:  # noqa
        """Проверка пароля."""
        if password is None:
            raise ValueError("Пароль не должен быть пустым!")
        if not isinstance(password, (bytes, str)):
            raise TypeError("Пароль должен быть строкой или байтами!")
        return password

    @field_validator("birthday")
    def validate_birthday(cls, birthday: datetime) -> datetime:  # noqa
        """Преобразование даты рождения под нужный формат."""
        datetime_str = birthday.strftime("%Y-%m-%d %H:%M:%S")
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
