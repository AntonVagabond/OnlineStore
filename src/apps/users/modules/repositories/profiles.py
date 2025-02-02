from datetime import datetime
from types import NoneType
from typing import Optional, TypeAlias, Union
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import joinedload

from common.enums.role import RoleEnum
from common.exceptions import mixins as exception
from common.repositories.mixins import PaginatedPageRepository
from models import Role, User

RegisterData: TypeAlias = dict[str, Union[str, datetime, bool, RoleEnum, NoneType, UUID]]


class ProfileRepository(PaginatedPageRepository):
    """Репозиторий профиля пользователя."""

    model = User

    async def __is_exist_email(self, user_email: str) -> bool:
        """Проверка на существование пользователя с данным email в БД."""
        stmt = sa.select(self.model).filter(self.model.email.ilike(user_email))
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        return bool(result)

    async def __is_exist_phone_number(self, phone_number: str) -> bool:
        """Проверка на существование пользователя с данным телефонным номером в БД."""
        stmt = sa.select(self.model).filter(self.model.phone_number == phone_number)
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        return bool(result)

    async def __get_role_id(self, role: RoleEnum) -> UUID:
        """Получить идентификатор роли."""
        stmt = sa.select(Role.id).filter(Role.role == role.value)
        return (await self.session.execute(stmt)).scalar_one()

    async def add(self, data: RegisterData) -> str:
        """Добавить новую запись профиля в БД."""
        if await self.__is_exist_email(data["email"]):
            raise exception.EmailAlreadyExistsException()

        if await self.__is_exist_phone_number(data["phone_number"]):
            raise exception.PhoneNumberAlreadyExistsException()

        role_id = await self.__get_role_id(data.pop("role"))
        data.update(role_id=role_id)
        current_user_id = await super().add(data)
        return str(current_user_id)

    async def get(self, user_id: UUID) -> Optional[User]:
        """Получить профиль пользователя по идентификатору."""
        return await super().get(user_id)

    async def __get_stmt_for_auth(self, username: str) -> sa.Select:
        """Получить запрос микросервиса авторизации."""
        stmt = (
            sa.select(self.model)
            .options(joinedload(self.model.role).load_only(Role.name))
            .filter(self.model.deleted.__eq__(False), self.model.email == username)
        )
        return stmt

    async def get_user_by_login(self, username: str) -> Optional[User]:
        """Получить данные по логину пользователя."""
        stmt = await self.__get_stmt_for_auth(username)
        record = (await self.session.execute(stmt)).scalar_one_or_none()
        return record
