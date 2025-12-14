"""User <-> Child relationship link with metadata (mother, guardian, pickup, etc.)."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class ChildRelationshipType(str, Enum):
    mother = "mother"
    father = "father"
    guardian = "guardian"
    grandmother = "grandmother"
    grandfather = "grandfather"
    emergency_contact = "emergency_contact"
    authorized_pickup = "authorized_pickup"
    other = "other"


class ChildRelationship(Base):
    """Association object between a User and a Child."""

    __tablename__ = "child_relationships"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    child_id: Mapped[int] = mapped_column(
        ForeignKey("children.id", ondelete="CASCADE"),
        primary_key=True,
    )

    relationship_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default=ChildRelationshipType.guardian.value,
    )

    is_primary_contact: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="false",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # Bidirectional links
    user: Mapped["User"] = relationship(back_populates="child_relationships")
    child: Mapped["Child"] = relationship(back_populates="user_relationships")
