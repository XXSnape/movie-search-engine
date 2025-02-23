from collections.abc import Sequence

from aiogram.fsm.context import FSMContext
from cache.get_data import get_data_from_cache
from database.repository.favorite import FavoriteRepository
from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from utils.constants.cache_keys import FAVORITE_IDS_CACHE


async def add_movie_to_favorite(
    session: AsyncSession, cache: FSMContext, user_id: int, movie_id: int
) -> None:
    """
    Добавляет фильм в таблицу избранное

    :param session: сессия для работы с базой
    :param cache: кэш с данными
    :param user_id: id пользователя
    :param movie_id: id фильма
    :return: None
    """
    favorite_ids = await get_data_from_cache(FAVORITE_IDS_CACHE, cache=cache)
    favorite_ids.append(movie_id)
    await FavoriteRepository.create_object(
        session=session, data={"user_tg_id": user_id, "movie_id": movie_id}
    )


async def delete_movie_from_favorite(
    session: AsyncSession, cache: FSMContext, user_id: int, movie_id: int
) -> None:
    """
    Удаляет фильм их таблицы избранное

    :param session: сессия для работы с базой
    :param cache: кэш с данными
    :param user_id: id пользователя
    :param movie_id: id фильма
    :return: None
    """
    favorite_ids = await get_data_from_cache(FAVORITE_IDS_CACHE, cache=cache)
    favorite_ids.remove(movie_id)
    await FavoriteRepository.delete_object_by_params(
        session=session, data={"user_tg_id": user_id, "movie_id": movie_id}
    )


async def get_favorite_movies_by_user_id(
    session: AsyncSession, user_id: int
) -> Sequence[Row | RowMapping | int]:
    """
    Получает id фильмов в избранном
    :param session: сессия для работы с базой
    :param user_id: id пользователя
    :return:
    """
    return await FavoriteRepository.get_movie_ids(session=session, user_id=user_id)
