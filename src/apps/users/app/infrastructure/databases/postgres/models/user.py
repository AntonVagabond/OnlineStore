import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.common.models.base import Base
from app.infrastructure.common.models.mixins import CreatedUpdatedMixin, UUIDMixin


class User(Base, CreatedUpdatedMixin, UUIDMixin):
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

    profile: Mapped["Profile"] = relationship(  # type: ignore
        uselist=False, back_populates="user", lazy="raise"
    )
