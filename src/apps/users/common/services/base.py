from typing import TypeVar, Optional
from uuid import UUID

from common.interfaces.abstraction_service import IService
from common.models.base import Base
from common.schemas.filters.mixins import BaseFilterSchema
from common.schemas.internal.mixins import PageViewSchema
from common.unit_of_works.base import BaseUnitOfWork

TModel = TypeVar("TModel", bound=Base)
TDict = TypeVar("TDict", bound=dict)
TFilter = TypeVar("TFilter", bound=BaseFilterSchema)
TUnitOfWork = TypeVar("TUnitOfWork", bound=BaseUnitOfWork)
TID = TypeVar("TID", int, UUID)


class BaseService(IService):
    """Базовый класс сервиса."""

    @classmethod
    async def add(cls, uow: TUnitOfWork, obj_dict: TDict) -> TID:
        """Базовый метод сервиса для добавления данных."""
        async with uow:
            obj_id = await uow.repo.add(obj_dict)
            await uow.commit()
            return obj_id

    @classmethod
    async def get(cls, uow: TUnitOfWork, obj_id: TID) -> Optional[TModel]:
        """Базовый метод сервиса для получения данных."""
        async with uow:
            obj = await uow.repo.get(obj_id)
            return obj

    @classmethod
    async def get_all(
            cls, uow: TUnitOfWork, filters: Optional[TFilter],
    ) -> PageViewSchema:
        """Базовый метод сервиса для получения списка данных."""

    @classmethod
    async def delete(cls, uow: TUnitOfWork, obj_id: TID) -> Optional[TID]:
        """Базовый метод сервиса для обновления статуса данных на "удалено"."""
        async with uow:
            result = await uow.repo.delete(obj_id)
            await uow.commit()
            return result

    @classmethod
    async def delete_db(cls, uow: TUnitOfWork, obj_id: TID) -> bool:
        """Базовый метод сервиса для удаления данных из базы данных."""
        async with uow:
            result = await uow.repo.delete_db(obj_id)
            await uow.commit()
            return result

    @classmethod
    async def edit(cls, uow: TUnitOfWork, obj_dict: TDict) -> bool:
        """Базовый метод сервиса для редактирования данных."""
        async with uow:
            result = await uow.repo.edit(obj_dict)
            await uow.commit()
            return bool(result)

    @classmethod
    async def exist(cls, uow: TUnitOfWork, obj_id: TID) -> bool:
        """Базовый метод сервиса для поиска данных."""
        async with uow:
            result = await uow.repo.exist(obj_id)
            return result
