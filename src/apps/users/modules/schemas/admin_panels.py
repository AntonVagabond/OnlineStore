from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field

from common.enums.role import RoleEnum
from common.schemas.api.mixins import StandardViewSchemaForTable, UpdateSchema
from common.schemas.base import BaseModel
from common.schemas.filters.mixins import DataRangeBaseFilterSchema


class UserByRoleFilterSchema(DataRangeBaseFilterSchema):
    """Схема фильтра для пользователей по ролям."""

    role_uuid: Optional[UUID] = Field(default=None)


class UserViewSchemaForAdminTable(StandardViewSchemaForTable):
    """Схема представления пользователя для таблицы админа."""

    role: str


class UpdateAdminSchema(UpdateSchema):
    """Схема для редактирования пользователя Администратором."""

    id: Optional[UUID] = Field(default=None)
    role: RoleEnum


class UserResponseSchema(BaseModel):
    """Схема получения пользователя для его редактирования Администратором."""

    id: UUID
    last_name: Optional[str] = Field(default=None)
    first_name: Optional[str] = Field(default=None)
    second_name: Optional[str] = Field(default=None)
    is_man: bool = Field(default=True)
    birthday: Optional[datetime] = Field(default=None)
    photo: Optional[str]
    role: str
    role_id: UUID
