from datetime import date, datetime

from sqlalchemy import JSON, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserTgMixin


class RequestModel(UserTgMixin, Base):
    """
    Модель запроса
    """

    params: Mapped[dict] = mapped_column(JSON)
    page: Mapped[int]
    index: Mapped[int]
    command: Mapped[str]
    date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
