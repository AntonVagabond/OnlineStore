from abc import ABC, abstractmethod


class Transaction(ABC):
    """Псевдоним для Сессии БД."""

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
