from sqlalchemy import UUID, Column, String, Table

from .base import metadata

user_table = Table(
    "users",
    metadata,
    Column("user_id", UUID(as_uuid=True), primary_key=True),
    Column("username", String(length=100), unique=True, nullable=False),
    Column("email", String(length=256), unique=True, nullable=False, index=True),
    Column("phone_number", String(length=18), unique=True, nullable=True),
)
