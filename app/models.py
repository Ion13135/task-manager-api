from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TaskModel(Base):
    """Database table 'task',"""
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    completed: Mapped[bool] = mapped_column(default=False)
    priority: Mapped[int] = mapped_column(default=1)