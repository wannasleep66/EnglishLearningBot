from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    username: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    answers: Mapped["Answer"] = relationship(back_populates="user")
