from app.domain.user.events.user_created import UserCreated

from ..brokers.rabbit.message import Message
from ..common.serializers import json_dumps
from .integrations.integration_event import IntegrationEvent
from .integrations.user.user_created import user_created_to_integration

DomainEvents = UserCreated | ...


def domain_event_to_integration_event(event: DomainEvents) -> IntegrationEvent:
    """Преобразовать событие доменной модели в событие интеграции."""
    match event:
        case UserCreated():
            return user_created_to_integration(event)
        case _:
            raise ValueError(f"Неизвестный тип события: {event}")


def integration_event_to_message(event: IntegrationEvent) -> Message:
    """Преобразовать событие интеграции в сообщение."""
    return Message(message_id=event.event_id, data=json_dumps(event))
