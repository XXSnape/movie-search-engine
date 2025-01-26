from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, declared_attr, mapped_column


class UserTgMixin:
    """
    Миксин для добавления поля user_tg_id
    """

    @declared_attr
    def user_tg_id(cls) -> Mapped[int]:
        """
        Поле user_tg_id
        :return: Поле user_tg_id
        """
        return mapped_column(BigInteger)
