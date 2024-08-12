from datetime import datetime
from types import NoneType
from typing import Union, TypeAlias, Optional
from uuid import UUID

from common.enums.role import Role
from common.repositories.mixins import PaginatedPageRepository
from models.users import User

RegisterData: TypeAlias = dict[str, Union[str, datetime, bool, Role, NoneType]]


class ProfileRepository(PaginatedPageRepository[User]):
    """Репозиторий профиля пользователя."""

    async def get(self, user_id: UUID) -> Optional[User]:
        """Получить профиль пользователя по идентификатору."""
        return await super().get(user_id)
