from collections.abc import Iterator

from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_db() -> Iterator[Session]:
    """One DB session per request; closed after the response is sent."""
    with SessionLocal() as session:
        yield session
