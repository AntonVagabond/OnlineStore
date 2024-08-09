from typing import TypeVar, Optional
from uuid import UUID

from common.interfaces.abstraction_service import IService
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


class BaseService(IService):
    """Базовый класс сервиса."""

    async def add(self, uow: TUnitOfWork, obj: TSchema) -> TID:
        """Базовый метод сервиса для добавления данных."""
        obj_dict = obj.model_dump()
        async with uow:
            obj_id = await uow.repo.add(obj_dict)
            await uow.commit()
            return obj_id

    async def get(self, uow: TUnitOfWork, obj_id: TID) -> Optional[TModel]:
        """Базовый метод сервиса для получения данных."""
        async with uow:
            obj = await uow.repo.get(obj_id)
            return obj

    async def get_all(
            self, uow: TUnitOfWork, filters: Optional[TFilter],
    ) -> PageViewSchema:
        """Базовый метод сервиса для получения списка данных."""

    async def delete(self, uow: TUnitOfWork, obj_id: TID) -> Optional[TID]:
        """Базовый метод сервиса для обновления статуса данных на "удалено"."""
        async with uow:
            result = await uow.repo.delete(obj_id)
            await uow.commit()
            return result

    async def delete_db(self, uow: TUnitOfWork, obj_id: TID) -> bool:
        """Базовый метод сервиса для удаления данных из базы данных."""
        async with uow:
            result = await uow.repo.delete_db(obj_id)
            await uow.commit()
            return result

    async def edit(self, uow: TUnitOfWork, obj: TSchema) -> bool:
        """Базовый метод сервиса для редактирования данных."""
        obj_dict = obj.model_dump()
        async with uow:
            result = await uow.repo.edit(obj_dict)
            await uow.commit()
            return result

    async def exist(self, uow: TUnitOfWork, obj_id: TID) -> bool:
        """Базовый метод сервиса для поиска данных."""
        async with uow:
            result = await uow.repo.exist(obj_id)
            return result
