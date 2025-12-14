"""User model."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from backend.app.models.child import ParentChildLink


class User(Base):
    """User model for parents."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")

    child_relationships: Mapped[list["ChildRelationship"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    related_children: Mapped[list["Child"]] = relationship(
        secondary="child_relationships",
        viewonly=True,
    )


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
