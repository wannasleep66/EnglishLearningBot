from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base


class Topic(Base):
    __tablename__ = "topics"
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    answers: Mapped["Answer"] = relationship(back_populates="topic")
