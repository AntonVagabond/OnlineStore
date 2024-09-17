from datetime import datetime
from typing import TypeAlias, Union
from uuid import UUID

from common.exceptions import mixins as exception
from common.schemas.internal.mixins import PageViewSchema
from common.services.mixins import PaginatedPageService
from models import User
from modules.schemas.admin_panels import (
    UpdateAdminSchema,
    UserByRoleFilterSchema,
    UserResponseSchema,
    UserViewSchemaForAdminTable,
)
from modules.unit_of_works.admin_panels import AdminPanelUOW

EditData: TypeAlias = dict[str, Union[UUID, str, bool, datetime, int, None]]


class AdminPanelService(PaginatedPageService):
    """Сервис для работы админ панели."""

    # region --------------------------------- LIST --------------------------------------
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
                count_records, UserViewSchemaForAdminTable, list_records, filters
            )
            return response

    # endregion --------------------------------------------------------------------------

    @staticmethod
    def __convert_result(result: User) -> UserResponseSchema:
        """Конвертировать результат в pydantic-модель."""
        return UserResponseSchema(
            id=result.id,
            last_name=result.last_name,
            first_name=result.first_name,
            second_name=result.second_name,
            birthday=result.birthday,
            photo=result.photo,
            role=result.role.name,
            role_id=result.role_id,
        )

    async def get(self, uow: AdminPanelUOW, obj_id: UUID) -> UserResponseSchema:
        """Получить данные пользователя для редактирования."""
        async with uow:
            result = await uow.repo.get(obj_id)
            if result is None:
                raise exception.UserNotFoundException()
            response = self.__convert_result(result)
            return response

    # region ---------------------------------- EDIT -------------------------------------
    @staticmethod
    def __update_data(data: EditData) -> EditData:
        """Обновить данные пользователя."""
        last_name, first_name, second_name = (
            data["last_name"],
            data["first_name"],
            data["second_name"],
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

    # endregion --------------------------------------------------------------------------

    # region -------------------------------- DELETE -------------------------------------
    @classmethod
    async def delete(cls, uow: AdminPanelUOW, obj_id: UUID) -> UUID:
        """
        Удаление пользователя Администратором
        (установка статуса пользователя на "удален").
        """
        result = await super().delete(uow=uow, obj_id=obj_id)
        if result is None:
            raise exception.UserNotFoundException()
        return result

    # endregion --------------------------------------------------------------------------
