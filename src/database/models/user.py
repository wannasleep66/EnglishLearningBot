from datetime import datetime

from sqlalchemy import func, sql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    last_activity: Mapped[datetime] = mapped_column(
        default=datetime.now, server_default=func.now()
    )
    has_notifications: Mapped[bool] = mapped_column(
        default=False, server_default=sql.false()
    )
    answers: Mapped["Answer"] = relationship(back_populates="user")
