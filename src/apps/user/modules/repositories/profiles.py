from datetime import datetime
from types import NoneType
from typing import Union, TypeAlias

from common.enums.role import Role
from common.repositories.mixins import PaginatedPageRepository
from models.users import User

RegisterData: TypeAlias = dict[str, Union[str, datetime, bool, Role, NoneType]]


class ProfileRepository(PaginatedPageRepository[User]):
    """Репозиторий профиля пользователя."""
