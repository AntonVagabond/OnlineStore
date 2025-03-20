import abc
from typing import Protocol
from uuid import UUID


class IdGenerator(Protocol):
    @abc.abstractmethod
    def generate(self) -> UUID:
        raise NotImplementedError
