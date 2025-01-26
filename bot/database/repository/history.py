from datetime import date

from database.repository.abstract_repositories.manager_repository import (
    ManagerRepository,
)
from sqlalchemy import ScalarResult, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import HistoryModel


class HistoryRepository(ManagerRepository):
    """
    Репозиторий для работы с историей
    """

    model = HistoryModel

    @classmethod
    async def get_uniq_dates(cls, session: AsyncSession, user_id: int) -> ScalarResult:
        """
        Получает даты, в которых у пользователя есть история
        :param session: сессия для работы с базой
        :param user_id: id пользователя
        :return: уникальные даты
        """
        query = (
            select(cls.model.date)
            .filter_by(user_tg_id=user_id)
            .group_by(cls.model.date)
            .order_by(cls.model.date.asc())
        )
        result = await session.execute(query)
        return result.scalars()

    @classmethod
    async def delete_history_by_interval(
        cls, session: AsyncSession, user_id: int, start_date: date, last_date: date
    ) -> None:
        """
        Удаляет история по интервалу

        :param session: сессия для работы с базой
        :param user_id: id пользователя
        :param start_date: дата начала удаления
        :param last_date: дата конца удаления
        :return: None
        """
        stmt = delete(cls.model).filter(
            cls.model.date.between(start_date, last_date),
            cls.model.user_tg_id == user_id,
        )
        await session.execute(stmt)
        await session.commit()
