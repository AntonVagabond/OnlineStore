from app.domain.common.entity import Entity
from app.infrastructure.db.postgres.interfaces.data_mapper import DataMapper
from app.infrastructure.db.postgres.interfaces.registry import Registry


class RegistryImpl(Registry):
    """Класс реализующий регистрацию преобразователей данных для сущностей."""

    def __init__(self) -> None:
        self.__mappers: dict[type[Entity], type[DataMapper]] = {}

    def register_mapper(self, entity: type[Entity], mapper: type[DataMapper]) -> None:
        """Регистрируем сущность и его преобразователь данных в словарь."""
        self.__mappers[entity] = mapper

    def get_mapper_type(self, entity: type[Entity]) -> type[DataMapper]:
        """Получить преобразователь данных для сущности, которую укажем."""
        mapper_type = self.__mappers.get(entity)
        if not mapper_type:
            raise ValueError(
                f"Преобразователь данных для сущности {entity} не зарегистрирован!"
            )
        return mapper_type
