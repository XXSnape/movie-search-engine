from aiogram.fsm.context import FSMContext
from cache.data_for_cache import (
    MovieBigInfoCache,
    MovieFromAnotherProjectCache,
    MovieSmallInfoCache,
    Person,
)
from cache.get_data import get_data_from_cache
from config.settings import settings
from utils.constants.cache_keys import MAX_PAGE_CACHE, MOVIES_CACHE
from utils.enums.movie_data import ViewingMovieDetails


def get_projects(
    projects: list[int | MovieFromAnotherProjectCache],
    movie: MovieBigInfoCache,
    project_index: int,
) -> tuple[MovieFromAnotherProjectCache, str, int] | None:
    """
    Проверяет, хранятся ли в projects id или реальные объекты..

    :param projects: список из MovieFromAnotherProjectCache
    :param movie: MovieBigInfoCache
    :param project_index: текущий проект
    :return: MovieFromAnotherProjectCache, название фильма, количество всех проектов или None
    """
    if isinstance(projects[0], int) is False:
        return projects[project_index], movie.title, len(projects)


def get_persons(option: ViewingMovieDetails, movie: MovieBigInfoCache) -> list[Person]:
    """
    Получает людей (актеров или режиссеров) в зависимости от контекста
    :param option: ViewingMovieDetails
    :param movie: MovieBigInfoCache
    :return: список Person
    """
    data = ViewingMovieDetails
    if option in (data.ACTOR_PROJECTS, data.ACTORS, data.ACTOR_DETAILS):
        persons = movie.actors
    elif option in (data.DIRECTOR_PROJECTS, data.DIRECTORS, data.DIRECTOR_DETAILS):
        persons = movie.directors
    return persons


async def get_movies_by_download_type(
    cache: FSMContext,
    movies: list[MovieSmallInfoCache],
    download_type: ViewingMovieDetails | None,
):
    """
    Получает фильмы и заполняет кэш по типу загрузки, вставляя информацию в конец или начало списка
    :param cache: кэш с данными
    :param movies: список из MovieSmallInfoCache
    :param download_type: тип подгрузки
    :return: список из MovieSmallInfoCache
    """
    if download_type is None:
        current_movies = movies
    elif download_type == download_type.DOWNLOAD_FOLLOWING:
        current_movies = await get_data_from_cache(MOVIES_CACHE, cache=cache)
        current_movies.extend(movies)
    elif download_type == download_type.DOWNLOAD_PREVIOUS:
        current_movies = await get_data_from_cache(MOVIES_CACHE, cache=cache)
        current_movies = movies + current_movies
    return current_movies


async def get_movies_by_json_resp(
    cache: FSMContext,
    movies: list[MovieSmallInfoCache],
    json_resp: dict,
    download_type: ViewingMovieDetails | None,
    movie_index: int = 0,
):
    """
    Получает фильмы по данным из api

    :param cache: кэш с данными
    :param movies: список из MovieSmallInfoCache
    :param json_resp: данные из api
    :param download_type: тип подгрузки
    :param movie_index: индекс фильма
    :return: MovieSmallInfoCache и количество фильмов в кэше
    """
    current_movies = await get_movies_by_download_type(
        cache=cache, movies=movies, download_type=download_type
    )
    if download_type == ViewingMovieDetails.DOWNLOAD_PREVIOUS:
        movie_index = settings.API.NUMBER_FILMS - 1
    await cache.update_data(
        {MOVIES_CACHE: current_movies, MAX_PAGE_CACHE: json_resp["pages"]}
    )
    return movies[movie_index], len(current_movies)
