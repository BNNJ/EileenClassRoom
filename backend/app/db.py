from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

from app.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for database sessions.

    Configuration:
    - autocommit=False: Explicit commits required
    - autoflush=False: Explicit flushes required

    Yields:
        Database session that is automatically closed after use.
    """
    with Session(engine, autoflush=False) as session:
        yield session
