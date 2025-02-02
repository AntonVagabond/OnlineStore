from app.domain.common.entity import Entity
from app.infrastructure.databases.postgres.interfaces.data_mapper import DataMapper
from app.infrastructure.databases.postgres.interfaces.registry import Registry


class RegistryImpl(Registry):
    """Класс реализующий регистрацию преобразователей данных для сущностей."""

    def __init__(self) -> None:
        self.__mappers: dict[type[Entity], DataMapper] = {}

    def register_mapper(self, entity: type[Entity], mapper: DataMapper) -> None:
        """Регистрируем сущность и его преобразователь данных в словарь."""
        self.__mappers[entity] = mapper

    def get_mapper(self, entity: type[Entity]) -> DataMapper:
        """Получить преобразователь данных для сущности, которую укажем."""
        mapper = self.__mappers.get(entity)
        if not mapper:
            raise ValueError(
                f"Преобразователь данных для сущности {entity} не зарегистрирован!"
            )
        return mapper
