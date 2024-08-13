import base64
from datetime import datetime
from types import NoneType
from typing import Optional, Union, TypeAlias
from uuid import UUID

from common.enums.role import Role
from common.services.base import BaseService
from models.users import User
from modules.repositories.profiles import ProfileRepository
from modules.schemas.profile import ProfileResponseSchema
from modules.unit_of_works.profiles import ProfileUOW

RegisterData: TypeAlias = dict[
    str, Union[bytes, str, datetime, bool, Role, NoneType, int]
]
EditData: TypeAlias = dict[str, Union[UUID, str, bool, datetime, int, None]]


class ProfileService(BaseService):
    """Сервис для работы с профилем."""

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
    async def get(cls, uow: ProfileUOW, user_id: UUID) -> Optional[ProfileResponseSchema]:
        """Получить профиль пользователя."""
        async with uow:
            current_user = await uow.repo.get(user_id)
            return cls.__convert_result(current_user) if current_user else None
