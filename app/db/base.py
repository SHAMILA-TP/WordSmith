from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Parent class for all models. Alembic reads Base.metadata to see the tables."""
