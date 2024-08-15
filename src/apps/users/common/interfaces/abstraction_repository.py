from abc import ABC, abstractmethod
from datetime import datetime
from types import NoneType
from typing import TypeVar, TypeAlias, Union, Optional, Generic
from uuid import UUID

from sqlalchemy import ScalarResult

from common.enums.role import RoleEnum
from common.models.base import Base
from common.schemas.base import BaseModel
from common.schemas.filters.mixins import BaseFilterSchema

TModel = TypeVar("TModel", bound=Base)
TSchema = TypeVar("TSchema", bound=BaseModel)
TFilter = TypeVar("TFilter", bound=BaseFilterSchema)
TID = TypeVar("TID", int, UUID)

RegisterData: TypeAlias = dict[str, Union[str, datetime, bool, RoleEnum, NoneType]]
EditData: TypeAlias = dict[str, Union[UUID, str, bool, datetime, int, None]]


class IRepository(ABC):
    """Абстрактная класс репозитория."""
    model: type[TModel]

    @abstractmethod
    async def add(self, data: RegisterData) -> TID:
        """Абстрактный метод репозитория для добавления данных."""

    @abstractmethod
    async def get(self, data_id: TID) -> Optional[TModel]:
        """Абстрактный метод репозитория для получения данных."""

    @abstractmethod
    async def get_all(self, filters: TFilter) -> tuple[int, Optional[ScalarResult]]:
        """Абстрактный метод репозитория для получения списка данных."""

    @abstractmethod
    async def delete(self, data_id: TID) -> Optional[TID]:
        """Абстрактный метод репозитория для обновления статуса данных на "удалено"."""

    @abstractmethod
    async def delete_db(self, data_id: TID) -> bool:
        """Абстрактный метод репозитория для удаления данных из базы данных."""

    @abstractmethod
    async def edit(self, data: EditData) -> bool:
        """Абстрактный метод репозитория для редактирования данных."""

    @abstractmethod
    async def exist(self, obj_id: TID) -> bool:
        """Абстрактный метод репозитория для поиска данных."""
