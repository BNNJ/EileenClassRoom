from collections.abc import Generator
from typing import cast

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

from app.config import settings

engine = create_engine(cast(str, settings.DATABASE_URL), pool_pre_ping=True)


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        cls = self.__class__.__name__
        pk = getattr(self, "id", None)
        if pk is not None:
            return f"<{cls} id={pk}>"
        return f"<{cls} at 0x{id(self):x}>"



def get_db() -> Generator[Session, None, None]:
    """
    Dependency for database sessions.

    - Explicit commits are required for writes.
    - autoflush=False: no implicit flushes before queries.

    Yields:
        Database session that is automatically closed after use.
    """
    with Session(engine, autoflush=False) as session:
        yield session
