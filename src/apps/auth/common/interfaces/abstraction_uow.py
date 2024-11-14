import abc
from types import TracebackType
from typing import Optional, Self


class IUnitOfWork(abc.ABC):
    """Абстрактный класс для работы с транзакциями."""

    @abc.abstractmethod
    def __init__(self) -> None: ...

    @abc.abstractmethod
    async def __aenter__(self) -> Self:
        """Абстрактный метод входа в контекстного менеджера."""

    @abc.abstractmethod
    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Абстрактный метод выхода из контекстного менеджера"""

    @abc.abstractmethod
    async def close(self) -> None:
        """Абстрактный метод закрытия транзакции."""
