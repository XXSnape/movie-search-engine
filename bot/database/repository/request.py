from datetime import datetime, timedelta
from typing import Sequence

from config.settings import settings
from database.models import RequestModel
from database.repository.abstract_repositories.manager_repository import (
    ManagerRepository,
)
from sqlalchemy import Sequence, delete, select
from sqlalchemy.ext.asyncio import AsyncSession


class RequestRepository(ManagerRepository):
    """
    Репозиторий для работы с запросом
    """

    model = RequestModel
    text: str

    @classmethod
    async def delete_requests(cls, session: AsyncSession) -> None:
        """
        Удаляет информацию о запросах спустя 3 дня.

        :param session: сессия для работы с базой
        :return: None
        """
        last_date = datetime.now().date() - timedelta(
            days=settings.API.DAYS_BEFORE_DELETION
        )
        stmt = delete(cls.model).filter(
            cls.model.date < last_date,
        )
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def get_requests(
        cls, session: AsyncSession, data: dict
    ) -> Sequence[RequestModel]:
        """
        Получает запросы.
        Сортирует по дате в порядке убывания

        :param session: сессия для работы с базой
        :param data: cловарь с данными, по которым будет осуществлен поиск запросов

        :return: коллекция из RequestModel
        """
        query = select(cls.model).filter_by(**data).order_by(cls.model.date.desc())
        result = await session.execute(query)
        return result.scalars().all()
