from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from common.models.base import Base

TModel = TypeVar("TModel", bound=Base)


class BaseRepository:
    """Базовый класс репозитория."""

    model: type[TModel]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
