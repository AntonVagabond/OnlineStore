from typing import Optional
from uuid import UUID

from pydantic import Field

from common.enums.role import RoleEnum
from common.schemas.api.mixins import PersonBaseSchema, UpdateSchema
from common.schemas.filters.mixins import DataRangeBaseFilterSchema


class UserByRoleFilterSchema(DataRangeBaseFilterSchema):
    """Схема фильтра для пользователей по ролям."""
    role_uuid: Optional[UUID] = Field(default=None)


class UserViewSchemaForAdminTable(PersonBaseSchema):
    """Схема представления пользователя для таблицы админа."""
    role: str


class UpdateAdminSchema(UpdateSchema):
    """Схема для редактирования пользователя Администратором."""
    id: Optional[UUID] = Field(default=None)
    role: RoleEnum
