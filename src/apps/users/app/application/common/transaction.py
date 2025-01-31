import abc
from typing import Protocol


class UnitOfWorkTransaction(Protocol):
    """Протокол для работы с транзакциями."""

    @abc.abstractmethod
    async def commit(self) -> None:
        """Абстрактный метод фиксирования транзакции."""
        raise NotImplementedError
