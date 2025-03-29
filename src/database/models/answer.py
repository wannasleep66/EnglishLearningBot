from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Answer(Base):
    __tablename__ = "answers"
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    task: Mapped[str]
    is_correct: Mapped[bool]

    user: Mapped["User"] = relationship(back_populates="answers")
    topic: Mapped["Topic"] = relationship(back_populates="answers")
