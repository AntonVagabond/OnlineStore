from datetime import datetime
from typing import Union, TypeAlias
from uuid import UUID

from common.schemas.internal.mixins import PageViewSchema
from common.services.mixins import PaginatedPageService
from models import User
from modules.schemas.admin_panels import (
    UserByRoleFilterSchema, UserViewSchemaForAdminTable,
)
from modules.unit_of_works.admin_panels import AdminPanelUOW

EditData: TypeAlias = dict[str, Union[UUID, str, bool, datetime, int, None]]


class AdminPanelService(PaginatedPageService):
    """Сервис для работы админ панели."""

    @staticmethod
    def __convert_record(record: User) -> UserViewSchemaForAdminTable:
        """Конвертировать запись в pydantic-модель."""
        return UserViewSchemaForAdminTable(
            id=record.id,
            email=record.email,
            phone_number=record.phone_number,
            full_name=record.full_name,
            role=record.role.name,
        )

    async def get_all(
            self, uow: AdminPanelUOW, filters: UserByRoleFilterSchema
    ) -> PageViewSchema:
        """Получить информацию по фильтрам пользователей."""
        async with uow:
            count_records, records = await uow.repo.get_all(filters)
            if records is None:
                list_records = []
            else:
                list_records = [
                    self.__convert_record(record) for record in self._gen_records(records)
                ]
            response = self._get_response(
                count_records, UserViewSchemaForAdminTable, list_records, filters,
            )
            return response
