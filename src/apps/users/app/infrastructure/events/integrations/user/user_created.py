from dataclasses import dataclass
from typing import TypeVar
from uuid import UUID

from app.domain.user.events.user_created import UserCreated as UserCreatedDomainEvent

from ..integration_event import IntegrationEvent

IEV = TypeVar("IEV", bound=str)


@dataclass(frozen=True)
class UserCreatedIntegrationEvent(IntegrationEvent[IEV]):
    user_id: UUID
    email: str
    phone_number: str
    username: str


def user_created_to_integration(
    event: UserCreatedDomainEvent,
) -> UserCreatedIntegrationEvent:
    """Преобразовать событие создания пользователя в интеграционное событие."""
    return UserCreatedIntegrationEvent[event.event_type](
        event_id=event.event_uuid,
        event_date=event.event_date,
        user_id=event.user_id,
        email=event.email,
        phone_number=event.phone_number,
        username=event.username,
    )
