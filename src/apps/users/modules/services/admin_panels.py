from datetime import datetime
from typing import Union, TypeAlias
from uuid import UUID

from common.schemas.internal.mixins import PageViewSchema
from common.exceptions import mixins as exception
from common.services.mixins import PaginatedPageService
from models import User
from modules.schemas.admin_panels import (
    UserByRoleFilterSchema, UserViewSchemaForAdminTable, UpdateAdminSchema,
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

    @classmethod
    async def get_all(
            cls, uow: AdminPanelUOW, filters: UserByRoleFilterSchema
    ) -> PageViewSchema:
        """Получить информацию по фильтрам пользователей."""
        async with uow:
            count_records, records = await uow.repo.get_all(filters)
            if records is None:
                list_records = []
            else:
                list_records = [
                    cls.__convert_record(record) for record in cls._gen_records(records)
                ]
            response = cls._get_response(
                count_records, UserViewSchemaForAdminTable, list_records, filters,
            )
            return response

    @staticmethod
    def __update_data(data: EditData) -> EditData:
        """Обновить данные пользователя."""
        last_name, first_name, second_name = (
            data["last_name"], data["first_name"], data["second_name"]
        )
        data.update(full_name=f"{last_name} {first_name} {second_name}")
        return data

    @classmethod
    async def edit(cls, uow: AdminPanelUOW, obj: UpdateAdminSchema) -> bool:
        """Редактирование данных пользователя Администратором."""
        obj_dict = obj.model_dump()
        async with uow:
            if not await uow.repo.exist(obj_dict.get("id")):
                raise exception.UserNotFoundException()

            obj_dict = cls.__update_data(obj_dict)

            user_instance = await uow.repo.edit(obj_dict)
            await uow.commit()
            return bool(user_instance)
