from typing import Optional
from uuid import UUID

from pydantic import Field

from common.schemas.api.mixins import PersonBaseSchema
from common.schemas.filters.mixins import DataRangeBaseFilterSchema


class UserByRoleFilterSchema(DataRangeBaseFilterSchema):
    """Схема фильтра для пользователей по ролям."""
    role_uuid: Optional[UUID] = Field(default=None)


class UserViewSchemaForAdminTable(PersonBaseSchema):
    """Схема представления пользователя для таблицы админа."""
    role: str
