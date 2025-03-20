from typing import Protocol


class Commiter(Protocol):
    """Протокол для управления транзакциями."""

    async def commit(self) -> None:
        """Метод фиксирования транзакции."""
        raise NotImplementedError
