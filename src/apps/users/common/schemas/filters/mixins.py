from datetime import datetime
from typing import TypeVar, Optional

from pydantic import Field

from common.schemas.base import BaseModel
from core.config import get_settings

TSchema = TypeVar("TSchema", bound=BaseModel)

settings = get_settings()


class BaseFilterSchema(BaseModel):
    """Базовый фильтр-схема."""
    page_number: int = Field(ge=0, default=0, description="Номер страницы")
    page_size: int = Field(
        ge=1, le=100, default=settings.page_size, description="Размер страницы",
    )
    search_string: Optional[str] = Field(default=None, description="Строка поиска")


class DataRangeBaseFilterSchema(BaseFilterSchema):
    """Схема базового фильтра диапазона данных."""
    date_begin: Optional[datetime] = Field(default=None)
    date_end: Optional[datetime] = Field(default=None)
