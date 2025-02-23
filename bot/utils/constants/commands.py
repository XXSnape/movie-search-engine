"""
Модуль с доступными командами
"""

from config.settings import settings
from utils.constants.output_for_user import END_PREVIEW_OUTPUT
from utils.enums.commands import Commands

COMMANDS_AND_DESCRIPTIONS = (
    (Commands.MOVIE_SEARCH, "Предоставляет поиск фильма / сериала по названию"),
    (
        Commands.MOVIE_BY_PARAMS,
        "Предоставляет поиск фильмов / сериалов по разным параметрам."
        " Сортирует по рейтингу Кинопоиска или году выпуска в России",
    ),
    (
        Commands.MOVIE_BY_COLLECTIONS,
        "Предоставляет поиск фильмов по коллекциям. Сортирует по году выпуска",
    ),
    (
        Commands.MOVIE_IN_CINEMA,
        "Предоставляет поиск фильмов в кино. Сортирует по рейтингу Кинопоиска",
    ),
    (
        Commands.MOVIE_BY_STATUSES,
        "Предоставляет поиск фильмов / сериалов по этапам производства. Сортирует по количеству отзывов",
    ),
    (
        Commands.FAVORITE,
        "Фильмы в Избранном",
    ),
    (
        Commands.HISTORY,
        "Вся информацию о просмотренных фильмах сохраняется."
        " Ее можно посмотреть или удалить (по дате или целому промежутку времени)",
    ),
    (
        Commands.REQUESTS,
        f"Вместо того, чтобы проходить опросы заново и вновь смотреть на одни и те же фильмы,"
        f" информацию о них можно сохранить, нажав «{END_PREVIEW_OUTPUT}»."
        f" Они будут храниться в течение {settings.API.DAYS_BEFORE_DELETION} дней,"
        f" после чего будут удалены, чтобы данные всегда были актуальны",
    ),
)
