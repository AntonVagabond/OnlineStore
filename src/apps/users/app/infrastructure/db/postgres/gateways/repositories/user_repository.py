from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.common.unit_of_work import UnitOfWork
from app.domain.user.entities.user import User
from app.domain.user.repositories.user_repository import UserRepository

from ...converters import convert_to_entity as convert
from ...tables.user import users_table


class UserRepositoryImpl(UserRepository):
    """Класс реализации репозитория пользователя."""

    __slots__ = ("__uow", "__session")

    def __init__(self, uow: UnitOfWork, session: AsyncSession) -> None:
        self.__uow = uow
        self.__session = session

    def add(self, user: User) -> None:
        """Добавить пользователя зарегистрировав новую сущность."""
        self.__uow.register_new(user)

    def update(self, user: User) -> None:
        """Обновить пользователя зарегистрировав обновление сущности."""
        self.__uow.register_dirty(user)

    def delete(self, user: User) -> None:
        """Удалить пользователя зарегистрировав удаление сущности."""
        self.__uow.register_deleted(user)

    async def __get_convert_result_or_none(
        self,
        query: Select[tuple[users_table]],
    ) -> User | None:
        """Вспомогательный метод для получения конвертирующего результата либо None."""
        result = (await self.__session.execute(query)).mappings().fetchone()
        if result is not None:
            return convert.result_to_user_entity(result)

    async def get_by_id(self, user_id: UUID) -> User | None:
        """Реализация получения пользователя по идентификатору."""
        query = select(users_table).where(users_table.c.user_id.__eq__(user_id))
        return await self.__get_convert_result_or_none(query)

    async def is_exists_phone_number(self, phone_number: str) -> User | None:
        """Реализация проверки на существование номера телефона."""
        query = select(users_table).where(users_table.c.phone_number.__eq__(phone_number))
        return await self.__get_convert_result_or_none(query)

    async def is_exists_email(self, email: str) -> User | None:
        """Реализация проверки на существование почты."""
        query = select(users_table).where(users_table.c.email.ilike(email))
        return await self.__get_convert_result_or_none(query)

    async def is_exists_username(self, username: str) -> User | None:
        """Реализация проверки на существование никнейма у пользователя."""
        query = select(users_table).where(users_table.c.username.ilike(username))
        return await self.__get_convert_result_or_none(query)
