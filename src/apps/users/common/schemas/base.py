from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict


class BaseModel(_BaseModel):
    """Базовая pydantic-модель."""

    model_config = ConfigDict()
