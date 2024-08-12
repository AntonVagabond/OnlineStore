from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase


class Base(MappedAsDataclass, DeclarativeBase):
    """Базовая модель."""
