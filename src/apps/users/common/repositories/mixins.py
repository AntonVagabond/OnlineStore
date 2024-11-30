from typing import Optional, TypeVar

import sqlalchemy as sa
from sqlalchemy import ScalarResult, Select

from common.models.base import Base
from common.repositories.base import BaseRepository
from common.schemas.filters.mixins import BaseFilterSchema, DataRangeBaseFilterSchema

TModel = TypeVar("TModel", bound=Base)
TFilter = TypeVar("TFilter", bound=BaseFilterSchema)
TFilterData = TypeVar("TFilterData", bound=DataRangeBaseFilterSchema)


class PaginatedPageRepository(BaseRepository):
    """Общий репозиторий для разбивки данных на страницы."""

    model: type[TModel]

    def _is_there_start_and_end_date(self, stmt: Select, filters: TFilterData) -> Select:
        """Проверка на существование даты начала и окончания."""
        if filters.date_begin:
            stmt = stmt.filter(self.model.updated_at >= filters.date_begin.date())
        if filters.date_end:
            stmt = stmt.filter(self.model.updated_at <= filters.date_end.date())
        return stmt

    async def _get_count_records(self, stmt: Select) -> int:
        """Получить количество записей."""
        # Создаем под запрос из переданного выражения `stmt`.
        subquery = stmt.subquery()

        # Используем `func.count` для подсчета записей в подзапросе.
        count_records = (
            await self.session.execute(
                sa.select(sa.func.count().label("count")).select_from(subquery)
            )
        ).scalar_one()
        return count_records

    async def _is_there_records(
        self, count_records: int, stmt: Select, filters: TFilter
    ) -> Optional[ScalarResult]:
        """Проверка на существование записи."""
        if count_records != 0:
            total_pages = (count_records - 1) // filters.page_size

            # Устанавливаем page_number в последнюю страницу, если
            # запрошенная страница превышает количество доступных страниц
            page_number = min(filters.page_number, total_pages)
            records = (
                await self.session.execute(
                    stmt.order_by(self.model.updated_at.desc())
                    .offset(page_number * filters.page_size)
                    .limit(filters.page_size)
                )
            ).scalars()
            return records
