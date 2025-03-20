from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.common.dto.user_dto import UserDto
from app.application.common.persistence.user_reader import UserReader

from ...converters import convert_to_dto as convert
from ...tables.user import users_table


class UserReaderImpl(UserReader):
    """Класс реализации чтения пользователей."""

    __slots__ = ("__session",)

    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def get_user(self, user_id: UUID) -> UserDto | None:
        """Реализация получения пользователя."""
        query = select(users_table).where(users_table.c.user_id.__eq__(user_id))
        result = (await self.__session.execute(query)).scalar_one_or_none()
        if result is not None:
            return convert.result_to_user_dto(result)
