from enum import StrEnum

from utils.constants.output_for_user import (
    CINEMA_OUTPUT,
    FAVORITE_OUTPUT,
    HISTORY_OUTPUT,
    SEARCH_OUTPUT,
)


class Commands(StrEnum):
    MOVIE_SEARCH = f"Искать фильм{SEARCH_OUTPUT}"
    MOVIE_BY_PARAMS = "Расширенный поиск🕵🏻"
    MOVIE_BY_COLLECTIONS = "Сборник фильмов📚"
    MOVIE_IN_CINEMA = f"Фильмы в кино{CINEMA_OUTPUT}"
    MOVIE_BY_STATUSES = "Фильмы в производстве🎬"
    FAVORITE = f"Избранное{FAVORITE_OUTPUT}"
    HISTORY = f"История{HISTORY_OUTPUT}"
    REQUESTS = "Запросы📨"
