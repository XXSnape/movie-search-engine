from datetime import timedelta

from config.settings import settings
from database.models import RequestModel
from utils.constants.api_data import (
    CINEMA_KEY,
    COLLECTION_KEY,
    COUNTRY_KEY,
    GENRE_KEY,
    NETWORK_KEY,
    STATUS_KEY,
    TYPE_KEY,
    TYPES,
    YEAR_SORT,
)
from utils.response_formats import join_by_sep
from utils.response_formats.pretty_response import get_russian_date
from utils.survey_data import API_CINEMAS
from utils.survey_data.collections import ALL_COLLECTIONS
from utils.survey_data.statuses import STATUSES
from utils.validators import get_value


def get_data_from_params(request: RequestModel) -> dict[str, str]:
    """
    Конвертирует данные из параметров запроса в читаемый вид
    :param request: RequestModel
    :return: dict[str, str]
    """
    russian_date = get_russian_date(request.date + timedelta(hours=3))
    collections = request.params.get(COLLECTION_KEY)
    collection_text = ALL_COLLECTIONS[collections[0][1:]] if collections else None
    return {
        "Дата запроса по Москве": russian_date,
        "Команда": request.command,
        "Просмотрено фильмов": (request.page - 1) * settings.API.NUMBER_FILMS
        + request.index
        + 1,
        "Коллекция": collection_text,
        "Жанры": join_by_sep(clear_pluses(request.params.get(GENRE_KEY))),
        "Страны": join_by_sep(clear_pluses(request.params.get(COUNTRY_KEY))),
        "Производители": join_by_sep(clear_pluses(request.params.get(NETWORK_KEY))),
        "Типы": join_by_sep(
            TYPES[type]
            for type in clear_pluses(get_value(TYPE_KEY, json=request.params))
        ),
        "Статусы": join_by_sep(
            STATUSES[status]
            for status in clear_pluses(get_value(STATUS_KEY, json=request.params))
        ),
        "Онлайн - кинотеатры": get_cinemas(request.params),
        "Годы": request.params.get(YEAR_SORT),
    }


def clear_pluses(strings: list[str] | None) -> list[str] | tuple:
    """
    Убирает + перед элементами
    :param strings: строки
    :return: list[str] | tuple
    """
    if not strings:
        return ()
    return [string[1:] if string[0] == "+" else string for string in strings]


def get_cinemas(params: dict) -> str:
    """
    Обрабатывает строку с онлайн-кинотеатрами для вывода
    :param params: параметры запроса
    :return: str
    """
    cinemas = params.get(CINEMA_KEY)
    if cinemas is not None and len(cinemas) > len(API_CINEMAS):
        return "Любая платформа"
    return join_by_sep(clear_pluses(cinemas))
