from aiogram.fsm.context import FSMContext
from cache.data_for_cache import MovieBigInfoCache, MovieSmallInfoCache
from utils.enums.movie_data import ViewingMovieDetails

from ..utils.get_objects import get_movies_by_json_resp
from .movie_cache import MovieCache
from .movie_mixins import MovieApiMixin
from .movie_processing import get_big_info, get_small_info


class MovieSearch(MovieApiMixin):
    """
    Класс для отправки базовых запросов на api для получения фильмов
    """

    @classmethod
    async def get_movie_and_length_by_title(
        cls,
        cache: FSMContext,
        params: dict,
        download_type: ViewingMovieDetails | None = None,
    ) -> tuple[MovieSmallInfoCache, int] | None:
        """
        Отправляет запрос на получение информации о фильме по названию.
        Записывает информацию в кэш

        :param cache: кэш с данными
        :param params: дополнительные параметры запроса
        :param download_type: тип загрузки, если нужно подгрузить еще
        :return: MovieSmallInfoCache, количество фильмов в кэше или None, если ничего не найдено
        """
        json_resp = await cls._make_request(url="search", params=params)
        if json_resp is None or cls._validate_response(json_resp) is False:
            return None
        movies = [get_small_info(movie) for movie in json_resp["docs"]]
        return await get_movies_by_json_resp(cache, movies, json_resp, download_type)

    @classmethod
    async def get_movie_by_id(
        cls, movie_id: int, cache: FSMContext
    ) -> MovieBigInfoCache | None:
        """
        Отправляет запрос на получение информации о фильме по его id.
        Записывает информацию в кэш

        :param movie_id: id фильма
        :param cache: кэш с данными
        :return: MovieBigInfoCache или None, если ничего не найдено
        """
        movie = await MovieCache.get_movie_by_id(movie_id=movie_id, cache=cache)
        if movie:
            return movie
        json_resp = await cls._make_request(url=movie_id)
        movie_info: MovieBigInfoCache = get_big_info(json_resp)
        await cache.update_data({str(movie_id): movie_info})
        return movie_info
