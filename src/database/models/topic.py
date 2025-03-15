from sqlalchemy.orm import Mapped, relationship

from .base import Base


class Topic(Base):
    __tablename__ = "topics"
    name: Mapped[str]
    description: Mapped[str]
    answers: Mapped["Answer"] = relationship(back_populates="topic")
