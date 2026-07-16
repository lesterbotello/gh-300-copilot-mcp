"""ORM models for the high school management system."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

try:
    from .database import Base
except ImportError:  # pragma: no cover - fallback for direct execution
    from database import Base


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), primary_key=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(50), default="member", nullable=False)
    grade_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class Activity(Base):
    __tablename__ = "activities"

    name: Mapped[str] = mapped_column(String(255), primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    schedule: Mapped[str] = mapped_column(String(255), nullable=False)
    max_participants: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    registrations: Mapped[list["Registration"]] = relationship(
        back_populates="activity",
        cascade="all, delete-orphan",
        order_by="Registration.created_at",
    )


class Registration(Base):
    __tablename__ = "registrations"
    __table_args__ = (
        UniqueConstraint("activity_name", "email", name="uq_registration_activity_email"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    activity_name: Mapped[str] = mapped_column(
        ForeignKey("activities.name", ondelete="CASCADE"),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        ForeignKey("users.email", ondelete="CASCADE"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    activity: Mapped[Activity] = relationship(back_populates="registrations")
    user: Mapped[User] = relationship()


class Complaint(Base):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="open", nullable=False)
    activity_name: Mapped[str | None] = mapped_column(
        ForeignKey("activities.name", ondelete="SET NULL"),
        nullable=True,
    )
    submitted_by_email: Mapped[str | None] = mapped_column(
        ForeignKey("users.email", ondelete="SET NULL"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    feedback_items: Mapped[list["Feedback"]] = relationship(
        back_populates="complaint",
        cascade="all, delete-orphan",
    )


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    complaint_id: Mapped[int] = mapped_column(
        ForeignKey("complaints.id", ondelete="CASCADE"),
        nullable=False,
    )
    author_email: Mapped[str | None] = mapped_column(
        ForeignKey("users.email", ondelete="SET NULL"),
        nullable=True,
    )
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    complaint: Mapped[Complaint] = relationship(back_populates="feedback_items")
    author: Mapped[User] = relationship()
