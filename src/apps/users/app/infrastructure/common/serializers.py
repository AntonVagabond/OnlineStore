import json
from datetime import date, datetime
from typing import Any
from uuid import UUID


class CustomJsonEncoder(json.JSONEncoder):
    """Класс для сериализации объектов в json."""

    def default(self, obj: object) -> Any:
        """Метод для изменения типов перед сериализацией в json."""
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime | date):
            return obj.isoformat()
        elif isinstance(obj, bytes):
            return obj.decode("ascii")


def json_dumps(data: Any) -> bytes | str:
    """Перевод данных в формат json."""
    return json.dumps(obj=data, cls=CustomJsonEncoder)
