import math
from typing import Generator, Optional, TypeVar

from sqlalchemy import ScalarResult

from common.models.base import Base
from common.schemas.base import BaseModel
from common.schemas.filters.mixins import BaseFilterSchema
from common.schemas.internal.mixins import PageViewSchema
from common.services.base import BaseService

TModel = TypeVar("TModel", bound=Base)
TFilter = TypeVar("TFilter", bound=BaseFilterSchema)
TViewSchemaForTable = TypeVar("TViewSchemaForTable", bound=BaseModel)


class PaginatedPageService(BaseService):
    """Общий сервис для разбивки данных на страницы."""

    @staticmethod
    def _gen_records(records: ScalarResult) -> Generator[TModel, None, None]:
        """Генератор записей."""
        yield from records

    @staticmethod
    def _get_response(
        count_records: int,
        schema: type[TViewSchemaForTable],
        list_records: list[Optional[TViewSchemaForTable]],
        filters: TFilter,
    ) -> PageViewSchema:
        """Получите ответ."""
        return PageViewSchema[schema](
            page=filters.page_number,
            max_page_count=math.ceil(count_records / filters.page_size) - 1,
            count_records=count_records,
            records=list_records,
        )
