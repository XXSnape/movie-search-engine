from collections.abc import Sequence

from database.models import FavoriteModel
from database.repository.abstract_repositories.manager_repository import (
    ManagerRepository,
)
from sqlalchemy import Row, RowMapping, select
from sqlalchemy.ext.asyncio import AsyncSession


class FavoriteRepository(ManagerRepository):
    """
    Репозиторий для работы с избранным
    """

    model = FavoriteModel

    @classmethod
    async def get_movie_ids(
        cls, session: AsyncSession, user_id: int
    ) -> Sequence[Row | RowMapping | int]:
        """
        Получает id фильмов по id юзера.
        Сортирует по дате в порядке убывания

        :param session: сессия для работы с базой
        :param user_id: id пользователя
        :return: коллекция из id фильмов
        """
        query = (
            select(cls.model.movie_id)
            .filter_by(user_tg_id=user_id)
            .order_by(cls.model.date.desc())
        )
        ids = await session.execute(query)
        return ids.scalars().all()
