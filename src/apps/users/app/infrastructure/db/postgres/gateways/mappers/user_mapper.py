from sqlalchemy import delete, insert, update
from sqlalchemy.ext.asyncio import AsyncConnection

from app.domain.user.entities.user import User

from ...converters import convert_to_dict as convert
from ...interfaces.data_mapper import DataMapper
from ...models.user import UserModel


class UserDataMapper(DataMapper):
    """Преобразователь данных для сущности User."""

    def __init__(self, connection: AsyncConnection) -> None:
        self.__connection = connection

    async def add(self, entity: User) -> None:
        """Добавление новой сущности в базу данных."""
        values = convert.user_entity_to_dict(entity)
        stmt = insert(UserModel).values(values)
        await self.__connection.execute(stmt)

    async def update(self, entity: User) -> None:
        """Обновление существующей сущности в базе данных."""
        values = convert.user_entity_to_dict(entity)
        stmt = update(UserModel).where(UserModel.id == entity.entity_id).values(values)
        await self.__connection.execute(stmt)

    async def delete(self, entity: User) -> None:
        """Удаление существующей сущности из базы данных."""
        stmt = delete(UserModel).where(UserModel.id == entity.entity_id)
        await self.__connection.execute(stmt)
