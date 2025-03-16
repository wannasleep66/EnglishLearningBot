from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    username: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    last_activity: Mapped[str] = mapped_column(
        default=datetime.now, server_default=func.now()
    )
    answers: Mapped["Answer"] = relationship(back_populates="user")
