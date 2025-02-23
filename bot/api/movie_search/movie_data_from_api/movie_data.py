from utils.constants.api_data import TYPES
from utils.response_formats import (
    get_amount_in_rubles,
    get_pretty_date,
    get_pretty_length_movie,
    get_pretty_number,
    join_by_sep,
)
from utils.survey_data.collections import ALL_COLLECTIONS
from utils.validators import get_value, get_value_by_different_keys


class MovieDataApi:
    """
    Класс с функциями, связанными с фильмами, достающими данные из ответа api
    """

    @classmethod
    def get_basic_information_dict(cls, json: dict) -> dict[str, str]:
        """
        Получает базовую информацию о фильме

        :param json: данные из api
        :return: словарь с данными в читаемом виде
        """
        data = {
            "Название": json.get("name"),
            "Год производства": get_value("year", json=json),
            "Краткое описание": get_value("shortDescription", json=json),
            "Страны": join_by_sep(
                country["name"] for country in json.get("countries", ())
            ),
            "Жанры": join_by_sep(genre["name"] for genre in json.get("genres", ())),
            "Рейтинг Кинопоиска": get_value("rating", "kp", json=json),
            "Возрастной рейтинг": get_value(
                "ageRating", json=json, format_result="{}+"
            ),
            "Длительность одной серии": get_pretty_length_movie(
                get_value("seriesLength", json=json)
            ),
            "Длительность": get_pretty_length_movie(
                get_value("movieLength", json=json)
            ),
        }
        return data

    @classmethod
    def get_addiction_information_dict(cls, json: dict) -> dict[str, str]:
        """
        Получает расширенную информацию о фильме

        :param json: данные из api
        :return: словарь с данными в читаемом виде
        """
        budget = get_pretty_number(
            get_amount_in_rubles(
                get_value("budget", "value", json=json),
                get_value("budget", "currency", json=json),
            )
        )
        fees = get_pretty_number(
            get_amount_in_rubles(
                get_value("fees", "russia", "value", json=json)
                or get_value("fees", "world", "value", json=json)
                or get_value("fees", "usa", "value", json=json),
                get_value("fees", "russia", "currency", json=json)
                or get_value("fees", "world", "currency", json=json)
                or get_value("fees", "usa", "currency", json=json),
            )
        )
        views = get_pretty_number(get_value("audience", 0, "count", json=json))
        return {
            "Полное описание": json.get("description"),
            "Количество просмотров": views,
            "Приблизительные сборы (в рублях)": fees,
            "Приблизительный бюджет (в рублях)": budget,
            "Слоган": get_value("slogan", json=json),
            "Тип": TYPES.get(json.get("type")),
            "Коллекции": join_by_sep(
                ALL_COLLECTIONS.get(collection)
                for collection in json.get("lists", ())
                if ALL_COLLECTIONS.get(collection)
            ),
            "Производители": join_by_sep(
                network["name"]
                for network in get_value(
                    "networks", "items", json=json, return_result=()
                )
            ),
            "Дата выхода": get_pretty_date(
                get_value_by_different_keys(
                    "russia", "world", "digital", json=json.get("premiere", {})
                )
            ),
        }

    @classmethod
    def get_related_projects_id(cls, key: str, json: dict) -> list[int]:
        """
        Получает id фильмов, связанных с другим (похожие, продолжения)

        :param key: ключ для обращения к данными из api
        :param json: данные из api
        :return: список с id фильмов
        """
        return [project["id"] for project in json.get(key, ())]

    @classmethod
    def get_watchability(cls, json: dict) -> list[list[str, str]]:
        """
        Получает сервисы для просмотра фильмов

        :param json: данные из api
        :return: список из списков, состоящих из названия онлайн-кинотеатров и их url
        """
        return [
            [resource["name"], resource["url"]]
            for resource in get_value(
                "watchability", "items", json=json, return_result=()
            )
        ]
