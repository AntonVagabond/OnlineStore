from typing import TYPE_CHECKING

import converters as convert

from ..brokers.rabbit.interfaces.publisher import IMessagePublisher

if TYPE_CHECKING:
    from app.application.common.event_bus import IEventBus
    from app.domain.common.event import Event


class EventBus(IEventBus):
    """Класс реализующий введение журнала событий"""

    def __init__(self, message_publisher: IMessagePublisher) -> None:
        self.message_publisher = message_publisher

    async def publish(self, domain_events: list[Event]) -> None:
        """Отправить события в очередь."""
        for domain_event in domain_events:
            # Конвертируем событие доменной модели в событие интеграционной модели
            integration_event = convert.domain_event_to_integration_event(domain_event)
            message = convert.integration_event_to_message(integration_event)
            await self.message_publisher.publish(
                message=message, key=integration_event.event_type
            )
