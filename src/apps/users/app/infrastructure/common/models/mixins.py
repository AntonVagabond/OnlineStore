import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column


class UUIDMixin:
    """Общая модель, для переопределения поля id типа integer на поле uuid4."""

    id: Mapped[UUID] = mapped_column(
        UUID,
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
    )


class CreatedUpdatedMixin:
    """Общая модель для указания времени создания и обновления."""

    created_at: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False)
