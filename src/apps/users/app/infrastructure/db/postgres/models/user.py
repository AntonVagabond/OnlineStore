import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import CreatedUpdatedMixin, UUIDMixin


class UserTable(Base, CreatedUpdatedMixin, UUIDMixin):
    """Модель пользователя."""

    username: Mapped[str | None] = mapped_column(
        sa.String(length=100), unique=True, nullable=False
    )
    email: Mapped[str | None] = mapped_column(
        sa.String(length=256),
        index=True,
        unique=True,
        nullable=False,
    )
    phone_number: Mapped[str | None] = mapped_column(sa.String(length=18), nullable=False)

    profile: Mapped["ProfileTable"] = relationship(  # type: ignore
        uselist=False, back_populates="user", lazy="raise"
    )
