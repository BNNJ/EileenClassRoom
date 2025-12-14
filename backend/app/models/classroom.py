"""Classroom model."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Classroom(Base):
    """Represents a classroom for a given school year."""

    __tablename__ = "classrooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    school_year_start: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    name: Mapped[str | None] = mapped_column(String(120), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Children currently in this classroom
    children: Mapped[list["Child"]] = relationship(back_populates="classroom")

    @property
    def school_year_label(self) -> str:
        return f"{self.school_year_start}-{self.school_year_start + 1}"
