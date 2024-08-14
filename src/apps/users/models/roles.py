from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.base import Base
from common.models.mixins import GenericMixin


class Role(Base, GenericMixin[sa.UUID]):
    """Модель ролей пользователей."""
    __tablename__ = "RoleDB"

    name: Mapped[Optional[str]] = mapped_column(
        __name_pos="Name",
        __type_pos=sa.String(256),
    )
    role: Mapped[int] = mapped_column(
        __name_pos="Role",
        __type_pos=sa.Integer,
        nullable=False,
    )
    users: Mapped[list["User"]] = relationship(  # type: ignore
        back_populates="role",
        lazy="raise",
    )
