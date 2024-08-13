from typing import TypeVar, Generic

from common.models.base import Base
from sqlalchemy.ext.asyncio import AsyncSession

TModel = TypeVar("TModel", bound=Base)


class BaseRepository:
    """Базовый класс репозитория."""
    model: type[TModel]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
