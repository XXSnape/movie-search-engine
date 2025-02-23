from api.movie_search.movie_data_from_api.movie_data import MovieDataApi
from api.person_search.person_processing import get_actors_and_directors
from cache.data_for_cache import (
    MovieBigInfoCache,
    MovieFromAnotherProjectCache,
    MovieSmallInfoCache,
)
from utils.constants.error_data import NO_PHOTO
from utils.response_formats import build_text, present_data
from utils.validators import get_value


def get_small_info(json: dict) -> MovieSmallInfoCache:
    """
    Конвертирует базовую информацию о фильме в MovieSmallInfoCache
    :param json: данные из api
    :return: MovieSmallInfoCache
    """
    text, photo = __get_text_and_photo(json)
    return MovieSmallInfoCache(text=text, photo=photo, movie_id=json["id"])


def get_movie_by_id(id: int, movies: list[MovieSmallInfoCache]) -> MovieSmallInfoCache:
    """
    Получает фильм из списка фильмов в соответствии с его id
    :param id: id нужного фильма
    :param movies: список с фильмами
    :return: MovieSmallInfoCache
    """
    for movie in movies:
        if movie.movie_id == id:
            return movie


def get_movie_from_another_project_info(
    json: dict, num: int, is_sequel: bool
) -> MovieFromAnotherProjectCache:
    """
    Конвертирует информацию о фильме, связанным с текущим в MovieFromAnotherProjectCache

    :param json: данные из api
    :param num: часть фильма
    :param is_sequel: True, если фильм является продолжением
    :return: MovieFromAnotherProjectCache
    """
    text, photo = __get_text_and_photo(json)
    if is_sequel:
        text = build_text(f"Номер {num}\n\n") + text
    watchability = MovieDataApi.get_watchability(json)
    return MovieFromAnotherProjectCache(
        movie_id=json["id"], text=text, photo=photo, watchability=watchability
    )


def get_big_info(json: dict[str, str | int]) -> MovieBigInfoCache:
    """
    Конвертирует расширенную информацию о фильме в MovieBigInfoCache
    :param json: данные из api
    :return: MovieBigInfoCache
    """
    data = MovieDataApi.get_basic_information_dict(json)
    data.update(MovieDataApi.get_addiction_information_dict(json))

    text = present_data(data)
    title = data["Название"]
    watchability = MovieDataApi.get_watchability(json)
    sequels = MovieDataApi.get_related_projects_id("sequelsAndPrequels", json)
    similar_projects = MovieDataApi.get_related_projects_id("similarMovies", json)
    actors, directors = get_actors_and_directors(json)
    return MovieBigInfoCache(
        movie_id=json["id"],
        title=title,
        text=text,
        watchability=watchability,
        actors=actors,
        directors=directors,
        sequels=sequels,
        similar_projects=similar_projects,
    )


def __get_text_and_photo(json: dict) -> tuple[str, str]:
    """
    Получает текст и фото фильма

    :param json: данные из api
    :return: текст и фото фильма
    """
    text = present_data(MovieDataApi.get_basic_information_dict(json))
    photo = get_value("poster", "url", json=json) or NO_PHOTO
    return text, photo
