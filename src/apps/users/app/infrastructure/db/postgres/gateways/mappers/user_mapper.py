from sqlalchemy import delete, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.user.entities.user import User

from ...converters import convert_to_dict as convert
from ...interfaces.data_mapper import DataMapper
from ...models.user import UserTable


class UserDataMapper(DataMapper):
    """Преобразователь данных для сущности User."""

    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def add(self, entity: User) -> None:
        """Добавление новой сущности в базу данных."""
        values = convert.user_entity_to_dict(entity)
        stmt = insert(UserTable).values(values)
        await self.__session.execute(stmt)

    async def update(self, entity: User) -> None:
        """Обновление существующей сущности в базе данных."""
        values = convert.user_entity_to_dict(entity)
        stmt = update(UserTable).where(UserTable.id == entity.entity_id).values(values)
        await self.__session.execute(stmt)

    async def delete(self, entity: User) -> None:
        """Удаление существующей сущности из базы данных."""
        stmt = delete(UserTable).where(UserTable.id == entity.entity_id)
        await self.__session.execute(stmt)
