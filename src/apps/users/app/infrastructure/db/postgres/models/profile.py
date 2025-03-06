from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import CreatedUpdatedMixin, UUIDMixin


class ProfileTable(Base, CreatedUpdatedMixin, UUIDMixin):
    """Модель профиля пользователя."""

    user_id: Mapped[sa.UUID] = mapped_column(
        sa.UUID, sa.ForeignKey(column="user_table.id", ondelete="CASCADE")
    )
    last_name: Mapped[str | None] = mapped_column(sa.String(length=100))
    first_name: Mapped[str | None] = mapped_column(sa.String(length=100))
    second_name: Mapped[str | None] = mapped_column(sa.String(length=100))
    photo: Mapped[str | None] = mapped_column(sa.String(length=100))
    birthday: Mapped[datetime | None] = mapped_column(sa.DateTime)
    bio: Mapped[bool] = mapped_column(sa.Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(sa.String(length=25), nullable=False)

    user: Mapped["User"] = relationship(  # type: ignore
        back_populates="profile", lazy="raise"
    )
