from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# One engine per process; it owns the connection pool.
engine = create_engine(settings.database_url, pool_pre_ping=True)

# Factory for sessions (one session = one unit of work / transaction scope).
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
