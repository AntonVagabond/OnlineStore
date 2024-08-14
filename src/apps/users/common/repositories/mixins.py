from typing import TypeVar, Optional

import sqlalchemy as sa
from sqlalchemy import Select, ScalarResult

from common.models.base import Base
from common.repositories.base import BaseRepository
from common.schemas.filters.mixins import BaseFilterSchema, DataRangeBaseFilterSchema

TModel = TypeVar("TModel", bound=Base)
TFilter = TypeVar("TFilter", bound=BaseFilterSchema)
TFilterData = TypeVar("TFilterData", bound=DataRangeBaseFilterSchema)


class PaginatedPageRepository(BaseRepository):
    """Общий репозиторий для разбивки данных на страницы."""
    model: type[TModel]

    def _is_there_start_and_end_date(
            self, stmt: Select, filters: TFilterData
    ) -> Select:
        """Проверка на существование даты начала и окончания."""
        if filters.date_begin:
            stmt = stmt.filter(self.model.date_update >= filters.date_begin.date())
        if filters.date_end:
            stmt = stmt.filter(self.model.date_update <= filters.date_end.date())
        return stmt

    async def _get_count_records(self, stmt: Select) -> int:
        """Получить количество записей."""
        count_records = (await self.session.execute(
            sa.select(sa.func.count(stmt.c.Id))
        )).scalar_one()
        return count_records

    async def _is_there_records(
            self, count_records: int, stmt: Select, filters: TFilter,
    ) -> Optional[ScalarResult]:
        """Проверка на существование записи."""
        if count_records != 0:
            records = (await self.session.execute(
                stmt
                .order_by(self.model.date_update.desc())
                .offset(
                    (
                        filters.page_number - 1
                        if filters.page_number > 0 else
                        filters.page_number
                    ) * filters.page_size)
                .limit(filters.page_size)
            )).scalars()
            return records
