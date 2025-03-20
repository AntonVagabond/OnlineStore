from abc import ABC, abstractmethod


class Transaction(ABC):
    """Псевдоним для AsyncSession."""

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
