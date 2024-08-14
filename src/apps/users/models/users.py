from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.mixins import DateModelMixin, GenericMixin


class User(DateModelMixin, GenericMixin[sa.UUID]):
    """Модель пользователя."""
    __tablename__ = "UserDB"

    username: Mapped[Optional[str]] = mapped_column(
        __name_pos="UserName",
        __type_pos=sa.String(100),
    )
    last_name: Mapped[Optional[str]] = mapped_column(
        __name_pos="LastName",
        __type_pos=sa.String(100),
    )
    first_name: Mapped[Optional[str]] = mapped_column(
        __name_pos="FirstName",
        __type_pos=sa.String(100),
    )
    second_name: Mapped[Optional[str]] = mapped_column(
        __name_pos="SecondName",
        __type_pos=sa.String(100),
    )
    full_name: Mapped[Optional[str]] = mapped_column(
        __name_pos="FullName",
        __type_pos=sa.String(200),
    )
    email: Mapped[Optional[str]] = mapped_column(
        __name_pos="Email",
        __type_pos=sa.String(256),
        unique=True,
    )
    password_hash: Mapped[Optional[bytes]] = mapped_column(
        __name_pos="PasswordHash",
        __type_pos=sa.LargeBinary,
    )
    phone_number: Mapped[Optional[str]] = mapped_column(
        __name_pos="PhoneNumber",
        __type_pos=sa.String(18),
    )
    photo: Mapped[Optional[str]] = mapped_column(
        __name_pos="Photo",
        __type_pos=sa.String(100),
    )
    birthday: Mapped[Optional[datetime]] = mapped_column(
        __name_pos="Birthday",
        __type_pos=sa.DateTime,
    )
    role: Mapped["Role"] = relationship(  # type: ignore
        back_populates="users",
        lazy="raise",
        default=None,
    )
    logged_out: Mapped[bool] = mapped_column(
        __name_pos="LoggedOut",
        __type_pos=sa.Boolean,
        default=False,
        nullable=False
    )
    deleted: Mapped[bool] = mapped_column(
        __name_pos="Deleted",
        __type_pos=sa.Boolean,
        default=False,
        nullable=False
    )
    is_man: Mapped[bool] = mapped_column(
        __name_pos="IsMan",
        __type_pos=sa.Boolean,
        default=False,
        nullable=False,
    )
    role_id: Mapped[Optional[sa.UUID]] = mapped_column(
        "RoleId",
        sa.UUID,
        sa.ForeignKey(column="RoleDB.Id", ondelete="RESTRICT"),
        default=None,
    )
