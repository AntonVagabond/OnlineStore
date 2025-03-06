from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TRequest = TypeVar("TRequest", contravariant=True)
TResponse = TypeVar("TResponse", covariant=True)


class Handler(Generic[TRequest, TResponse], ABC):
    @abstractmethod
    async def handle(self, request: TRequest) -> TResponse:
        """Обработка запроса."""
        raise NotImplementedError
