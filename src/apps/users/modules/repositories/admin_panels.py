from datetime import datetime
from typing import Union, TypeAlias, Optional
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import joinedload

from common.repositories.mixins import PaginatedPageRepository
from models import Role
from models.users import User
from modules.schemas.admin_panels import UserByRoleFilterSchema

EditData: TypeAlias = dict[str, Union[UUID, str, bool, datetime, int, None]]


class AdminPanelRepository(PaginatedPageRepository):
    """Репозиторий панели администратора."""
    model = User

    def __get_stmt_for_method_list(self) -> sa.Select:
        """Получить запрос для метода списка."""
        stmt = (
            sa.select(self.model)
            .options(joinedload(self.model.role).load_only(Role.name))
            .where(self.model.deleted.__eq__(False))
        )
        return stmt

    def __is_there_role(
            self, stmt: sa.Select, filters: UserByRoleFilterSchema
    ) -> sa.Select:
        """Проверка на существование роли"""
        if filters.role_uuid is not None:
            stmt = stmt.filter(self.model.role_id == filters.role_uuid)
        return stmt

    def __is_there_search_string(
            self, stmt: sa.Select, filters: UserByRoleFilterSchema,
    ) -> sa.Select:
        """Проверка на существование строки поиска."""
        if filters.search_string:
            stmt = stmt.filter(sa.or_(
                self.model.full_name.ilike(f"%{filters.search_string}%"),
                self.model.email.ilike(f"%{filters.search_string}"),
                self.model.phone_number.ilike(f"%{filters.search_string}%"),
                self.model.role.has(Role.name.ilike(f"%{filters.search_string}%")),
            ))
        return stmt

    async def get_all(
            self, filters: UserByRoleFilterSchema
    ) -> tuple[int, Optional[sa.ScalarResult]]:
        """Получить всех пользователей с учетом фильтра по роли."""
        stmt = self.__get_stmt_for_method_list()
        stmt = self.__is_there_role(stmt, filters)
        stmt = self.__is_there_search_string(stmt, filters)
        stmt = self._is_there_start_and_end_date(stmt, filters)
        count_records = await self._get_count_records(stmt)
        records = await self._is_there_records(count_records, stmt, filters)
        return count_records, records
