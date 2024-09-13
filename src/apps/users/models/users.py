from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.base import Base
from common.models.mixins import CreatedUpdatedMixin, UUIDMixin


class User(Base, CreatedUpdatedMixin, UUIDMixin):
    """Модель пользователя."""

    username: Mapped[Optional[str]] = mapped_column(sa.String(length=100))
    last_name: Mapped[Optional[str]] = mapped_column(sa.String(length=100))
    first_name: Mapped[Optional[str]] = mapped_column(sa.String(length=100))
    second_name: Mapped[Optional[str]] = mapped_column(sa.String(length=100))
    full_name: Mapped[Optional[str]] = mapped_column(sa.String(length=200))
    email: Mapped[Optional[str]] = mapped_column(
        sa.String(length=256), index=True, unique=True
    )
    password_hash: Mapped[Optional[bytes]] = mapped_column(sa.LargeBinary)
    phone_number: Mapped[Optional[str]] = mapped_column(sa.String(length=18))
    photo: Mapped[Optional[str]] = mapped_column(sa.String(length=100))
    birthday: Mapped[Optional[datetime]] = mapped_column(sa.DateTime)
    role: Mapped["Role"] = relationship(  # type: ignore
        back_populates="users", lazy="raise"
    )
    logged_out: Mapped[bool] = mapped_column(sa.Boolean, default=False, nullable=False)
    deleted: Mapped[bool] = mapped_column(sa.Boolean, default=False, nullable=False)
    is_man: Mapped[bool] = mapped_column(sa.Boolean, default=False, nullable=False)
    role_id: Mapped[Optional[sa.UUID]] = mapped_column(
        sa.UUID,
        sa.ForeignKey(column="role.id", ondelete="RESTRICT"),
        default=None,
    )
