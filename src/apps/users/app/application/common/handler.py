from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TRequest = TypeVar("TRequest", contravariant=True)
TResponse = TypeVar("TResponse", covariant=True)


class CommandHandler(Generic[TRequest, TResponse], ABC):
    """Класс для обработки команд."""

    @abstractmethod
    async def handle(self, command: TRequest) -> TResponse:
        """Обработка запроса."""
        raise NotImplementedError


class QueryHandler(Generic[TRequest, TResponse], ABC):
    """Класс для обработки запросов."""

    @abstractmethod
    async def handle(self, query: TRequest) -> TResponse:
        """Обработка запроса."""
        raise NotImplementedError
