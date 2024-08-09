import abc
from typing import Any, Optional, TypeVar
from uuid import UUID

from common.models.base import Base
from common.schemas.base import BaseModel
from common.schemas.filters.mixins import BaseFilterSchema
from common.schemas.internal.mixins import PageViewSchema
from common.unit_of_works.base import BaseUnitOfWork

TModel = TypeVar("TModel", bound=Base)
TSchema = TypeVar("TSchema", bound=BaseModel)
TFilter = TypeVar("TFilter", bound=BaseFilterSchema)
TUnitOfWork = TypeVar("TUnitOfWork", bound=BaseUnitOfWork)
TID = TypeVar("TID", int, UUID)


class IService(abc.ABC):
    """Абстрактный класс сервиса."""

    @abc.abstractmethod
    async def add(self, uow: TUnitOfWork, obj: TSchema) -> Any:
        """Абстрактный метод сервиса для добавления данных."""

    @abc.abstractmethod
    async def get(self, uow: TUnitOfWork, obj_id: TID) -> Optional[TModel]:
        """Абстрактный метод сервиса для получения данных."""

    @abc.abstractmethod
    async def get_all(
            self, uow: TUnitOfWork, filters: Optional[TFilter],
    ) -> PageViewSchema:
        """Абстрактный метод сервиса для получения списка данных."""

    @abc.abstractmethod
    async def delete(self, uow: TUnitOfWork, obj_id: TID) -> Optional[TID]:
        """Абстрактный метод сервиса для обновления статуса данных на "удалено"."""

    @abc.abstractmethod
    async def delete_db(self, uow: TUnitOfWork, obj_id: TID) -> bool:
        """Абстрактный метод сервиса для удаления данных из базы данных."""

    @abc.abstractmethod
    async def edit(self, uow: TUnitOfWork, obj: TSchema) -> bool:
        """Абстрактный метод сервиса для редактирования данных."""

    @abc.abstractmethod
    async def exist(self, uow: TUnitOfWork, obj_id: TID) -> bool:
        """Абстрактный метод сервиса для поиска данных."""
