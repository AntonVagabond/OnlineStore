from typing import Generic, TypeVar

from pydantic import Field

from common.schemas.base import BaseModel

TSchema = TypeVar("TSchema", bound=BaseModel)


class PageSchema(BaseModel, Generic[TSchema]):
    """Схема страницы."""
    count_records: int = Field(ge=0, default=0)
    records: list[TSchema]


class PageViewSchema(PageSchema[TSchema]):
    """Схема представления страницы."""
    page: int = Field(ge=0, default=0)
    max_page_count: int
