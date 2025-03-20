from sqlalchemy import UUID, Column, DateTime, ForeignKey, String, Table

from .base import metadata

profiles_table = Table(
    "profiles",
    metadata,
    Column("profile_id", UUID, primary_key=True),
    Column("user_id", ForeignKey("users.user_id"), unique=True),
    Column("first_name", String(length=100), nullable=False),
    Column("last_name", String(length=100), nullable=True),
    Column("second_name", String(length=100), nullable=True),
    Column("photo", String(length=100), nullable=True),
    Column("bio", String(length=18), nullable=False),
    Column("status", String(length=18), nullable=False),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=False),
)
