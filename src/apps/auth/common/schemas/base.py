from typing import Any

from pydantic import BaseModel as _BaseModel


class BaseModel(_BaseModel):
    """Базовая pydantic-модель."""

    class Config:
        @staticmethod
        def json_schema_extra(schema: dict[str, Any], _: Any) -> None:
            props = {}
            for key, value in schema.get("properties", {}).items():
                if not value.get("hidden", False):
                    props[key] = value
            schema["properties"] = props
