import uuid
from datetime import datetime
from typing import (
    Any, get_origin, get_args, ClassVar, TYPE_CHECKING, Self, TypeVar, Generic
)

import sqlalchemy as sa
from sqlalchemy import Integer, BigInteger, SmallInteger, UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import MappedAsDataclass, declared_attr
from sqlalchemy.orm import mapped_column

from common.models.base import Base

TInt = TypeVar("TInt", bound=Integer)


class GenericMixin(MappedAsDataclass, Generic[TInt]):
    __type_t: ClassVar[type[TInt]]  # noqa

    def __init_subclass__(cls, **kwargs: dict[str, Any]) -> None:
        """
        Метод находит базовый класс, являющийся наследником GenericMixin, и
        извлекает из него тип TInt, который затем сохраняется в __type_t.
        """
        orig_bases: list[type[Self]] = [
            orig_base for orig_base in cls.__orig_bases__  # type: ignore[attr-defined]
            if get_origin(orig_base) is GenericMixin
        ]
        assert len(orig_bases) == 1
        orig_base = orig_bases[0]
        # Получите тип T из аннотаций к типу.
        generic_types = get_args(orig_base)
        assert len(generic_types) == 1
        cls.__type_t = generic_types[0]

        super().__init_subclass__(**kwargs)

    def __id_impl(cls) -> Mapped[TInt]:  # noqa
        """
        Метод определяет, как будет создан столбец id в таблице базы данных
        в зависимости от типа TInt, заданного для текущего класса.
        """
        type_mapping = {
            int: Integer, BigInteger: BigInteger, SmallInteger: SmallInteger, UUID: UUID,
        }
        assert cls.__type_t in type_mapping, "Тип не поддерживается."
        if isinstance(type_mapping[cls.__type_t], sa.UUID):
            return mapped_column(
                __name_pos="Id",
                __type_pos=type_mapping[cls.__type_t],
                primary_key=True,
                unique=True,
                nullable=False,
                init=False,
                default=uuid.uuid4
            )
        return mapped_column(
            __name_pos="Id",
            __type_pos=type_mapping[cls.__type_t],
            primary_key=True,
            unique=True,
            autoincrement=True,
            nullable=False,
            init=False,
        )

    if TYPE_CHECKING:
        id: Mapped[TInt] = mapped_column(
            __name_pos="Id",
            __type_pos=Integer,
            primary_key=True,
            unique=True,
            autoincrement=True,
            nullable=False,
            init=False,
        )
    else:
        @declared_attr
        def id(cls) -> Mapped[TInt]:  # noqa
            return cls.__id_impl(cls)  # noqa


class DateModelMixin(Base):
    """Общая модель для создания и обновления."""
    __abstract__ = True
    date_add: Mapped[datetime] = mapped_column(
        __name_pos="DateAdd",
        __type_pos=sa.DateTime,
        nullable=False,
    )
    date_update: Mapped[datetime] = mapped_column(
        __name_pos="DateUpdate",
        __type_pos=sa.DateTime,
        nullable=False,
    )
