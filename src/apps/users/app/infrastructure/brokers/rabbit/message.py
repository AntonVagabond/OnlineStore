from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Message:
    message_id: UUID = field(default=uuid4())
    event_type: str = field(default="")
    data: str | bytes = field(default=b"")
