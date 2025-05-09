from typing import TypeVar

from app.domain.user.events.user_created import UserCreated

from ...domain.common.event import Event
from ..brokers.rabbit.message import Message
from ..common.serializers import json_dumps
from .integrations.integration_event import IntegrationEvent
from .integrations.user.user_created import user_created_to_integration

TDomainEvents = TypeVar("TDomainEvents", bound=Event)


def domain_event_to_integration_event(event: TDomainEvents) -> IntegrationEvent:
    """Преобразовать событие доменной модели в событие интеграции."""
    match event:
        case UserCreated():
            return user_created_to_integration(event)
        case _:
            raise ValueError(f"Неизвестный тип события: {event}")


def integration_event_to_message(event: IntegrationEvent) -> Message:
    """Преобразовать событие интеграции в сообщение."""
    return Message(
        message_id=event.event_id, event_type=event.event_type, data=json_dumps(event)
    )
