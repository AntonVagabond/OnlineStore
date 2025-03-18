from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass(frozen=True, kw_only=True)
class IntegrationEvent:
    event_id: UUID = field(default_factory=uuid4)
    event_date: datetime = field(default_factory=lambda: datetime.now(UTC))
    event_type: str
