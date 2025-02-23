from logging import getLogger
from typing import Any

from aiogram.fsm.context import FSMContext
from database.models import HistoryModel, RequestModel
from utils.constants.cache_keys import (
    FAVORITE_IDS_CACHE,
    REQUESTS_CACHE,
    WATCHED_MOVIES_CACHE,
)

logger = getLogger(name=__name__)


async def get_data_from_cache(key: str, cache: FSMContext) -> Any:
    """
    Получает данные из кэша по ключу

    :param key: ключ, по которому требуются данные
    :param cache: кэш с данными
    :return: возвращает данные, лежащие в кэше или None, если они не найдены
    """
    cache = await cache.get_data()
    if cache is not None:
        try:
            return cache[key]
        except (KeyError, IndexError):
            logger.info("Не найден ключ %s", key)
            return None


async def get_request_and_len(idx: int, cache: FSMContext) -> tuple[RequestModel, int]:
    """
    Получает RequestModel по индексу
    :param idx: индекс запроса
    :param cache: кэш с данными
    :return: RequestModel и количество запросов
    """
    data = await cache.get_data()
    return data[REQUESTS_CACHE][idx], len(data[REQUESTS_CACHE])


async def get_watched_movie_len_and_favorite_ids(
    idx: int, cache: FSMContext
) -> tuple[HistoryModel, int, list[int]]:
    """
    Получает HistoryModel по индексу
    :param idx: индекс фильма в истории
    :param cache: кэш с данными
    :return: HistoryModel, количество фильмов, id фильмов в избранном
    """
    data: dict = await cache.get_data()
    return (
        data[WATCHED_MOVIES_CACHE][idx],
        len(data[WATCHED_MOVIES_CACHE]),
        data[FAVORITE_IDS_CACHE],
    )
