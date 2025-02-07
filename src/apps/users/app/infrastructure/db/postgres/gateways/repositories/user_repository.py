from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncConnection

from app.domain.user.repositories.user_repository import IUserRepository

from ...converters import convert_to_entity as convert
from ...models.user import UserModel

if TYPE_CHECKING:
    from app.domain.user.entities.user import User


class UserRepository(IUserRepository):
    """Класс реализации репозитория пользователя."""

    def __init__(self, connection: AsyncConnection) -> None:
        self.__connection = connection

    async def __get_convert_result_or_none(
        self,
        query: Select[tuple[UserModel]],
    ) -> User | None:
        """Вспомогательный метод для получения конвертирующего результата либо None."""
        result = (await self.__connection.execute(query)).scalar_one_or_none()
        if result is not None:
            return convert.result_to_user_entity(result)

    async def load(self, user_id: UUID) -> User | None:
        """Реализация загрузки пользователя по идентификатору."""
        query = select(UserModel).where(UserModel.id == user_id)
        return await self.__get_convert_result_or_none(query)

    async def is_exists_phone_number(self, phone_number: str) -> User | None:
        """Реализация проверки на существование номера телефона."""
        query = select(UserModel).where(UserModel.phone_number == phone_number)
        return await self.__get_convert_result_or_none(query)

    async def is_exists_email(self, email: str) -> User | None:
        """Реализация проверки на существование почты."""
        query = select(UserModel).where(UserModel.email.ilike(email))
        return await self.__get_convert_result_or_none(query)

    async def is_exists_username(self, username: str) -> User | None:
        """Реализация проверки на существование никнейма у пользователя."""
        query = select(UserModel).where(UserModel.username.ilike(username))
        return await self.__get_convert_result_or_none(query)
