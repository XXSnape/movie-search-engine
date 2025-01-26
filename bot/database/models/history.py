from datetime import date

from sqlalchemy import Date, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserTgMixin


class HistoryModel(UserTgMixin, Base):
    """
    Модель истории
    """

    __tablename__ = "history"
    __table_args__ = (
        UniqueConstraint(
            "movie_id",
            "user_tg_id",
            "date",
            name="idx_uniq_user_movie_date",
        ),
    )
    movie_id: Mapped[int]
    text: Mapped[str] = mapped_column(Text)
    url: Mapped[str]
    date: Mapped[date] = mapped_column(Date, server_default=func.current_date())
