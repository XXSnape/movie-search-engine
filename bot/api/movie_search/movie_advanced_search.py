from typing import Any

from aiogram.fsm.context import FSMContext
from api.movie_search.movie_cache import MovieCache
from api.movie_search.movie_mixins import MovieApiMixin
from api.movie_search.movie_processing import (
    get_movie_by_id,
    get_movie_from_another_project_info,
)
from api.utils import MOVIE_PARAMS
from api.utils.get_objects import get_movies_by_json_resp
from cache.data_for_cache import MovieFromAnotherProjectCache, MovieSmallInfoCache
from utils.constants.cache_keys import MOVIES_CACHE
from utils.enums.movie_data import ViewingMovieDetails


class MovieAdvancedSearch(MovieApiMixin):
    """
    Класс для отправки запросов на api с большим количеством параметров
    """

    @classmethod
    async def get_related_movies_by_ids(
        cls,
        ids: list[int],
        sort_field: str | None = None,
        sort_type: int | None = None,
        is_sequel: bool = False,
    ) -> list[MovieFromAnotherProjectCache]:
        """
        Отправляет запрос на данные о фильмах, связанных с текущим

        :param ids: список с id связанных фильмов
        :param sort_field: поле, по которому проводить сортировку
        :param sort_type: тип сортировки
        :param is_sequel: True, если фильмы являются продолжениями, иначе False
        :return: список с информацией о связанных фильмов
        """
        params = {**MOVIE_PARAMS, "page": 1, "limit": len(ids), "id": ids}
        if sort_field:
            params["sortField"] = [sort_field]
        if sort_type:
            params["sortType"] = [sort_type]
        json_resp = await cls._make_request(params=params)
        return [
            get_movie_from_another_project_info(json, num, is_sequel)
            for num, json in enumerate(json_resp["docs"], 1)
        ]

    @classmethod
    async def get_movies_and_len_by_ids(
        cls, cache: FSMContext, ids: list[int]
    ) -> tuple[MovieSmallInfoCache, int]:
        """
        Отправляет запрос за получение данных о фильмах по их id.
        Записывает в кэш информацию о фильмах из api в соответствии с переданными id

        :param cache: кэш с данными
        :param ids: список с id фильмов
        :return: MovieSmallInfoCache и количество фильмов
        """
        params = {**MOVIE_PARAMS, "page": 1, "limit": len(ids), "id": ids}
        params.pop("notNullFields")  # так как нужны все фильмы, фильтрация не нужна
        json_resp = await cls._make_request(params=params)
        movies = await MovieCache.fill_in_with_movies(json_resp, cache)
        sorted_movies = [get_movie_by_id(id=id, movies=movies) for id in ids]
        await cache.update_data({MOVIES_CACHE: sorted_movies})
        return sorted_movies[0], len(sorted_movies)

    @classmethod
    async def get_movies_and_len_by_advanced_params(
        cls,
        cache: FSMContext,
        params: dict[str, Any],
        download_type: ViewingMovieDetails | None = None,
        movie_index: int = 0,
    ) -> tuple[MovieSmallInfoCache, int] | None:
        """
        Отправляет запрос с переданными параметрами.
        Записывает информацию в кэш

        :param cache: кэш с данными
        :param params: дополнительные параметры запроса
        :param download_type: тип загрузки, если нужно подгрузить фильмы
        :param movie_index: индекс фильма в списке фильмов
        :return: MovieSmallInfoCache и количество фильмов в кэше или None, если ничего не нашлось
        """
        params = {**MOVIE_PARAMS, **params}
        json_resp = await cls._make_request(params=params)
        if json_resp is None or cls._validate_response(json_resp) is False:
            return None
        movies = await MovieCache.fill_in_with_movies(json_resp, cache)
        return await get_movies_by_json_resp(
            cache, movies, json_resp, download_type, movie_index
        )
