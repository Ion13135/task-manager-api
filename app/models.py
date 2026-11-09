from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utc_now() -> datetime:
    """Current time in UTC (used as default for created_at columns)."""
    return datetime.now(timezone.utc)


class UserModel(Base):
    """Database table 'users'."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    # One user -> many tasks. If a user is deleted, their tasks are deleted too.
    tasks: Mapped[list["TaskModel"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )


class TaskModel(Base):
    """Database table 'tasks'."""
    __tablename__ = "tasks"


    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    completed: Mapped[bool] = mapped_column(default=False)
    priority: Mapped[int] = mapped_column(default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    # Foreign key: every task belongs to exactly one user
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped[UserModel] = relationship(back_populates="tasks")