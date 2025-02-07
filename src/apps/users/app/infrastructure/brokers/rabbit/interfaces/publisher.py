from abc import abstractmethod
from typing import Protocol

from ..message import Message


class IMessagePublisher(Protocol):
    """Протокол для публикации сообщений."""

    @abstractmethod
    async def publish(self, message: Message, key: str) -> None:
        """Публикация сообщения."""
        raise NotImplementedError
