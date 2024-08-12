from datetime import datetime
from types import NoneType
from typing import TypeVar, Optional, TypeAlias, Union
from uuid import UUID

from sqlalchemy import insert, select, update, delete, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from common.enums.role import Role
from common.interfaces.abstraction_repository import IRepository
from common.models.base import Base
from common.schemas.base import BaseModel
from common.schemas.filters.mixins import BaseFilterSchema

TModel = TypeVar("TModel", bound=Base)
TSchema = TypeVar("TSchema", bound=BaseModel)
TFilter = TypeVar("TFilter", bound=BaseFilterSchema)

RegisterData: TypeAlias = dict[str, Union[str, datetime, bool, Role, NoneType]]
EditData: TypeAlias = dict[str, Union[UUID, str, bool, datetime, int, None]]
TID = TypeVar("TID", int, UUID)


class BaseRepository(IRepository[TModel]):
    """Базовый класс репозитория."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, data: RegisterData) -> TID:
        """Базовый метод репозитория для добавления данных."""
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get(self, data_id: TID) -> Optional[TModel]:
        """Базовый метод репозитория для получения данных."""
        stmt = (
            select(self.model)
            .filter(
                self.model.id == data_id,
                self.model.deleted.__eq__(False),
                self.model.logged_out.__eq__(False),
            )
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_all(self, filters: TFilter) -> ScalarResult:
        """Базовый метод репозитория для получения списка данных."""

    async def delete(self, data_id: TID) -> Optional[TID]:
        """Базовый метод репозитория для обновления статуса данных на "удалено"."""
        stmt = (update(self.model)
                .filter(self.model.id == data_id, self.model.deleted.__eq__(False))
                .values(deleted=True, date_update=datetime.now())
                .returning(self.model.id))
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def delete_db(self, data_id: TID) -> bool:
        """Базовый метод репозитория для удаления данных из базы данных."""
        stmt = (delete(self.model)
                .where(self.model.id == data_id)
                .returning(self.model.id))
        res = await self.session.execute(stmt)
        return bool(res.scalar_one_or_none())

    async def edit(self, data: EditData) -> bool:
        """Базовый метод репозитория для редактирования данных."""
        data_id: TID = data.pop("id")
        stmt = (update(self.model)
                .filter(self.model.id == data_id, self.model.deleted.__eq__(False))
                .values(**data)
                .returning(self.model.id))
        res = await self.session.execute(stmt)
        return bool(res.scalar_one_or_none())

    async def exist(self, obj_id: TID) -> bool:
        """Базовый метод репозитория для поиска данных."""
        stmt = (select(self.model)
                .filter(self.model.id == obj_id, self.model.deleted.__eq__(False)))
        res = await self.session.execute(stmt)
        return bool(res.scalar_one_or_none())
