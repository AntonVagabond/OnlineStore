from pydantic import BaseModel as _BaseModel, ConfigDict


class BaseModel(_BaseModel):
    """Базовая pydantic-модель."""

    model_config = ConfigDict()
