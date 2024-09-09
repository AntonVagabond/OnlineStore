import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.base import Base
from common.models.mixins import UUIDMixin


class Role(Base, UUIDMixin):
    """Модель ролей пользователей."""
    name: Mapped[str] = mapped_column(
        sa.String(length=256), nullable=False, unique=True, index=True,
    )
    role: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    users: Mapped[list["User"]] = relationship(  # type: ignore
        back_populates="role", lazy="raise",
    )
