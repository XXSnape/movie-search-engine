from aiogram.fsm.context import FSMContext
from api.movie_search.movie_processing import get_big_info, get_small_info
from cache.data_for_cache import MovieBigInfoCache, MovieSmallInfoCache
from cache.get_data import get_data_from_cache
from utils.constants.cache_keys import MOVIES_CACHE


class MovieCache:
    """
    Класс для работы с кэшем
    """

    @classmethod
    async def get_small_info_movie_and_length_by_idx(
        cls, idx: int, cache: FSMContext
    ) -> tuple[MovieSmallInfoCache, int]:
        """
        Получает базовую информацию о фильме из кэша по индексу

        :param idx: индекс фильма в массиве фильмов
        :param cache: кэш с данными
        :return: MovieSmallInfoCache и количество фильмов в кэше
        """
        movies_cache: list[MovieSmallInfoCache] = await get_data_from_cache(
            MOVIES_CACHE, cache=cache
        )
        return movies_cache[idx], len(movies_cache)

    @classmethod
    async def get_movie_by_id(
        cls, movie_id: int, cache: FSMContext
    ) -> MovieBigInfoCache | None:
        """
        Получает полную информацию о фильме из кэша по его id
        :param movie_id: id фильма
        :param cache: кэш с данными
        :return: MovieBigInfoCache или None, если фильм не найден
        """
        movie_id = str(movie_id)
        movie: MovieBigInfoCache = await get_data_from_cache(movie_id, cache=cache)
        if movie is not None:
            return movie

    @classmethod
    async def fill_in_with_movies(
        cls, json_resp: dict, cache: FSMContext
    ) -> list[MovieSmallInfoCache]:
        """
        Заполняет кэш базовой информацией о фильмах из api

        :param json_resp: данные из api
        :param cache: кэш с данными
        :return: список MovieSmallInfoCache
        """
        movies = []
        for movie in json_resp["docs"]:
            movies.append(get_small_info(movie))
            await cache.update_data({str(movie["id"]): get_big_info(movie)})
        return movies
