from datetime import datetime

from sqlalchemy import DateTime, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserTgMixin


class FavoriteModel(UserTgMixin, Base):
    """
    Модель избранного
    """

    __tablename__ = "favorite"
    __table_args__ = (
        UniqueConstraint(
            "movie_id",
            "user_tg_id",
            name="idx_uniq_user_movie",
        ),
    )
    movie_id: Mapped[int]
    date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
