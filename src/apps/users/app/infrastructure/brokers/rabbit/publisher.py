import aio_pika

from ...common.serializers import json_dumps
from .interfaces.publisher import MessagePublisher
from .message import Message


class MessagePublisherImpl(MessagePublisher):

    __slots__ = ("__channel",)

    def __init__(self, channel: aio_pika.abc.AbstractChannel) -> None:
        self.__channel = channel

    @staticmethod
    def __build_message(message: Message) -> aio_pika.Message:
        """Создание AMQP сообщения."""
        return aio_pika.Message(
            body=json_dumps(message).encode("utf-8"),
            message_id=str(message.message_id),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

    async def publish(self, message: Message, exchange: str, routing_key: str) -> None:
        """Отправка сообщения в RabbitMQ."""
        amqp_message = self.__build_message(message)
        amqp_exchange = await self.__channel.get_exchange(name=exchange)
        await amqp_exchange.publish(message=amqp_message, routing_key=routing_key)
