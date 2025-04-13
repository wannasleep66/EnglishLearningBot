from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class TaskType(Base):
    __tablename__ = "task_types"

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]
