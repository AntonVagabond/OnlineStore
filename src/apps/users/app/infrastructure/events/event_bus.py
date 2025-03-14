from app.application.common.event_bus import EventBus
from app.domain.common.event import Event

from ..brokers.rabbit.config import Exchanges
from ..brokers.rabbit.interfaces.publisher import MessagePublisher
from .converters import domain_event_to_integration_event, integration_event_to_message


class EventBusImpl(EventBus):
    """Класс реализующий введение журнала событий"""

    def __init__(self, message_publisher: MessagePublisher) -> None:
        self.message_publisher = message_publisher

    async def publish(self, events: list[Event]) -> None:
        """Отправить события в очередь."""
        for domain_event in events:
            # Конвертируем событие доменной модели в событие интеграционной модели
            integration_event = domain_event_to_integration_event(domain_event)
            message = integration_event_to_message(integration_event)
            await self.message_publisher.publish(
                message=message,
                exchange=Exchanges.USER_EXCHANGE,
                routing_key=integration_event.event_type,
            )
