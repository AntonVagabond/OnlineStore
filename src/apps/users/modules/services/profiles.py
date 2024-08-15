from datetime import datetime
from types import NoneType
from typing import Union, TypeAlias
from uuid import UUID

from common.enums.role import RoleEnum
from common.exceptions import mixins as error
from common.schemas.api.mixins import RegisterSchema
from common.services.base import BaseService
from core.security import hash_password
from models.users import User
from modules.schemas.profiles import ProfileResponseSchema
from modules.unit_of_works.profiles import ProfileUOW

RegisterData: TypeAlias = dict[
    str, Union[bytes, str, datetime, bool, RoleEnum, NoneType, int]
]
EditData: TypeAlias = dict[str, Union[UUID, str, bool, datetime, int, None]]


class ProfileService(BaseService):
    """Сервис для работы с профилем."""

    # region --------------------------------- CREATE ------------------------------------
    @staticmethod
    def __add_user_data(user_data: RegisterData) -> RegisterData:
        """Добавить данные пользователя в БД."""
        user_data.update(username=user_data["email"])
        user_data.update(password_hash=hash_password(user_data["password_hash"]))
        last_name, first_name, second_name = (
            user_data['last_name'], user_data['first_name'], user_data['second_name'],
        )
        user_data.update(full_name=f"{last_name} {first_name} {second_name}")
        return user_data

    @classmethod
    async def create(cls, uow: ProfileUOW, schema: RegisterSchema) -> str:
        """Создать нового пользователя."""
        user_data = schema.model_dump()
        user_update_data = cls.__add_user_data(user_data)
        result = await cls.add(uow=uow, obj_dict=user_update_data)
        return result

    # endregion --------------------------------------------------------------------------

    # region ------------------------------- GET -----------------------------------------
    @staticmethod
    def __convert_result(result: User) -> ProfileResponseSchema:
        """Конвертировать результат в модель."""
        return ProfileResponseSchema(
            id=result.id,
            last_name=result.last_name,
            first_name=result.first_name,
            second_name=result.second_name,
            phone_number=result.phone_number,
            email=result.email,
            is_man=result.is_man,
            photo=result.photo if result.photo else None,
            birthday=result.birthday,
        )

    @classmethod
    async def get(cls, uow: ProfileUOW, user_id: UUID) -> ProfileResponseSchema:
        """Получить профиль пользователя."""
        async with uow:
            current_user = await uow.repo.get(user_id)
            if current_user is None:
                raise error.UserNotFoundException()
            return cls.__convert_result(current_user)

    # endregion --------------------------------------------------------------------------
