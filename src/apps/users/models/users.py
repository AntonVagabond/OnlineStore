from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.mixins import DateModelMixin, GenericMixin


class User(DateModelMixin, GenericMixin[sa.UUID]):
    """Модель пользователя."""
    __tablename__ = "Users"

    username: Mapped[Optional[str]] = mapped_column(
        __name_pos="user_name",
        __type_pos=sa.String(100),
    )
    last_name: Mapped[Optional[str]] = mapped_column(
        __name_pos="last_name",
        __type_pos=sa.String(100),
    )
    first_name: Mapped[Optional[str]] = mapped_column(
        __name_pos="first_name",
        __type_pos=sa.String(100),
    )
    second_name: Mapped[Optional[str]] = mapped_column(
        __name_pos="second_name",
        __type_pos=sa.String(100),
    )
    full_name: Mapped[Optional[str]] = mapped_column(
        __name_pos="full_name",
        __type_pos=sa.String(200),
    )
    email: Mapped[Optional[str]] = mapped_column(
        __name_pos="email",
        __type_pos=sa.String(256),
        unique=True,
    )
    password_hash: Mapped[Optional[bytes]] = mapped_column(
        __name_pos="password_hash",
        __type_pos=sa.LargeBinary,
    )
    phone_number: Mapped[Optional[str]] = mapped_column(
        __name_pos="phone_number",
        __type_pos=sa.String(18),
    )
    photo: Mapped[Optional[str]] = mapped_column(
        __name_pos="photo",
        __type_pos=sa.String(100),
    )
    birthday: Mapped[Optional[datetime]] = mapped_column(
        __name_pos="birthday",
        __type_pos=sa.DateTime,
    )
    role: Mapped["Role"] = relationship(  # type: ignore
        back_populates="users",
        lazy="raise",
        default=None,
    )
    logged_out: Mapped[bool] = mapped_column(
        __name_pos="logged_out",
        __type_pos=sa.Boolean,
        default=False,
        nullable=False
    )
    deleted: Mapped[bool] = mapped_column(
        __name_pos="deleted",
        __type_pos=sa.Boolean,
        default=False,
        nullable=False
    )
    is_man: Mapped[bool] = mapped_column(
        __name_pos="is_man",
        __type_pos=sa.Boolean,
        default=False,
        nullable=False,
    )
    role_id: Mapped[Optional[sa.UUID]] = mapped_column(
        "role_id",
        sa.UUID,
        sa.ForeignKey(column="Roles.id", ondelete="RESTRICT"),
        default=None,
    )
