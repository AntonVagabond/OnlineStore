from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Message:
    message_id: UUID = field(default=uuid4())
    event_type: datetime = field(default="")
    data: str | bytes = field(default=b"")
