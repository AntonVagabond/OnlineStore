import dataclasses
import json
from datetime import date, datetime
from typing import Any, TypeAlias
from uuid import UUID

Data: TypeAlias = dataclasses.dataclass or object


class CustomJsonEncoder(json.JSONEncoder):
    """Класс для сериализации объектов в json."""

    def default(self, obj: Data) -> Any:
        """Метод для изменения типов перед сериализацией в json."""
        if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
            return dataclasses.asdict(obj)
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime | date):
            return obj.isoformat()
        elif isinstance(obj, bytes):
            return obj.decode("ascii")


def json_dumps(data: Any) -> bytes | str:
    """Перевод данных в формат json."""
    return json.dumps(obj=data, cls=CustomJsonEncoder)
