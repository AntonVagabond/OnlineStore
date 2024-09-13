import abc
from typing import Any, Optional, TypeVar
from uuid import UUID

from common.models.base import Base
from common.schemas.filters.mixins import BaseFilterSchema
from common.schemas.internal.mixins import PageViewSchema
from common.unit_of_works.base import BaseUnitOfWork

TModel = TypeVar("TModel", bound=Base)
TDict = TypeVar("TDict", bound=dict)
TFilter = TypeVar("TFilter", bound=BaseFilterSchema)
TUnitOfWork = TypeVar("TUnitOfWork", bound=BaseUnitOfWork)
TID = TypeVar("TID", int, UUID)


class IService(abc.ABC):
    """Абстрактный класс сервиса."""

    @classmethod
    @abc.abstractmethod
    async def add(cls, uow: TUnitOfWork, obj_dict: TDict) -> Any:
        """Абстрактный метод сервиса для добавления данных."""

    @classmethod
    @abc.abstractmethod
    async def get(cls, uow: TUnitOfWork, obj_id: TID) -> Optional[TModel]:
        """Абстрактный метод сервиса для получения данных."""

    @classmethod
    @abc.abstractmethod
    async def get_all(
        cls, uow: TUnitOfWork, filters: Optional[TFilter]
    ) -> PageViewSchema:
        """Абстрактный метод сервиса для получения списка данных."""

    @classmethod
    @abc.abstractmethod
    async def delete(cls, uow: TUnitOfWork, obj_id: TID) -> Optional[TID]:
        """Абстрактный метод сервиса для обновления статуса данных на "удалено"."""

    @classmethod
    @abc.abstractmethod
    async def delete_db(cls, uow: TUnitOfWork, obj_id: TID) -> bool:
        """Абстрактный метод сервиса для удаления данных из базы данных."""

    @classmethod
    @abc.abstractmethod
    async def edit(cls, uow: TUnitOfWork, obj_dict: TDict) -> bool:
        """Абстрактный метод сервиса для редактирования данных."""

    @classmethod
    @abc.abstractmethod
    async def exist(cls, uow: TUnitOfWork, obj_id: TID) -> bool:
        """Абстрактный метод сервиса для поиска данных."""
