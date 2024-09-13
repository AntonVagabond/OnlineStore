from datetime import datetime
from types import NoneType
from typing import Union, TypeAlias
from uuid import UUID

from common.enums.role import RoleEnum
from common.exceptions import mixins as exception
from common.schemas.api.mixins import RegisterSchema
from common.services.base import BaseService
from core.security import hash_password
from models.users import User
from modules.schemas.profiles import ProfileResponseSchema, UpdateUserSchema
from modules.unit_of_works.profiles import ProfileUOW

RegisterData: TypeAlias = dict[
    str, Union[bytes, str, datetime, bool, RoleEnum, NoneType, int]
]
EditData: TypeAlias = dict[str, Union[UUID, str, bool, datetime, int, None]]


class ProfileService(BaseService):
    """Сервис для работы с профилем."""

    # region --------------------------------- CREATE ------------------------------------
    @staticmethod
    def __add_data_for_create(user_data: RegisterData) -> RegisterData:
        """Добавить данные для создания пользователя."""
        user_data.update(username=user_data["email"])
        user_data.update(password_hash=hash_password(user_data["password_hash"]))
        last_name, first_name, second_name = (
            user_data["last_name"], user_data["first_name"], user_data["second_name"]
        )
        user_data.update(full_name=f"{last_name} {first_name} {second_name}")
        return user_data

    @classmethod
    async def create(cls, uow: ProfileUOW, schema: RegisterSchema) -> str:
        """Создать нового пользователя."""
        user_data = schema.model_dump()
        user_update_data = cls.__add_data_for_create(user_data)
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
                raise exception.UserNotFoundException()
            return cls.__convert_result(current_user)

    # endregion --------------------------------------------------------------------------

    # region --------------------------------- EDIT --------------------------------------
    @staticmethod
    def __add_data_for_update(user_data: EditData, user_id: UUID) -> EditData:
        """Добавить данные для редактирования пользователя."""
        user_data.update(id=user_id)
        last_name, first_name, second_name = (
            user_data["last_name"], user_data["first_name"], user_data["second_name"]
        )
        user_data.update(full_name=f"{last_name} {first_name} {second_name}")
        return user_data

    @classmethod
    async def update(
            cls, uow: ProfileUOW, model: UpdateUserSchema, user_id: UUID
    ) -> bool:
        """Обновить данные пользователя."""
        user_data = model.model_dump()
        user_update_data = cls.__add_data_for_update(user_data, user_id)
        result = await cls.edit(uow=uow, obj_dict=user_update_data)
        return result

    # endregion --------------------------------------------------------------------------
