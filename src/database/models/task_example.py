from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class TaskExample(Base):
    __tablename__ = "task_examples"

    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"))
    task_type_id: Mapped[int] = mapped_column(
        ForeignKey("task_types.id", ondelete="CASCADE")
    )
    text: Mapped[str]

    topic: Mapped["Topic"] = relationship()
    task_type: Mapped["TaskType"] = relationship()

    __table_args__ = (
        UniqueConstraint(topic_id, task_type_id, name="topic_task_type_idx"),
    )
