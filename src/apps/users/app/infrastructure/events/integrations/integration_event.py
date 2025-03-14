from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Generic, TypeVar
from uuid import UUID, uuid4

IEV = TypeVar("IEV", bound=str)


@dataclass(frozen=True, kw_only=True)
class IntegrationEvent(Generic[IEV]):
    event_id: UUID = field(default_factory=uuid4)
    event_date: datetime = field(default_factory=lambda: datetime.now(UTC))
    event_type: IEV
