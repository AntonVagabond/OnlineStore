from uuid import UUID, uuid4

from app.domain.common.id_generator import IdGenerator


class IdGeneratorImpl(IdGenerator):
    def generate(self) -> UUID:
        """Генерация уникального идентификатора."""
        return uuid4()
