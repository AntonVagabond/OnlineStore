from dataclasses import dataclass
from uuid import UUID

from ...common.const import exceptions as text
from ...common.dto.user_dto import UserDto
from ...common.handler import QueryHandler
from ...common.persistence.user_reader import UserReader
from .. import exceptions as exc


@dataclass(frozen=True)
class GetUserQuery:
    user_id: UUID


class GetUserHandler(QueryHandler[GetUserQuery, UserDto]):
    """Класс-обработчик для получения пользователя."""

    def __init__(self, user_reader: UserReader) -> None:
        self.user_reader = user_reader

    async def handle(self, query: GetUserQuery) -> UserDto:
        """Получение пользователя."""
        user = await self.user_reader.get_user(query.user_id)
        if user is None:
            raise exc.UserNotFoundError(text.USER_NOT_FOUND)
        return user
