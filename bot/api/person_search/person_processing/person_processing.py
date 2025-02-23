from api.person_search.person_from_api.person_data import PersonDataAPI
from cache.data_for_cache import Person
from utils.response_formats import present_data


def get_actors_and_directors(json: dict) -> tuple[list[Person], list[Person]]:
    """
    Получает актеров и режиссеров
    :param json: данные из api
    :return: списки актеров и режиссеров
    """
    actors, directors = PersonDataAPI.get_actors_and_directors(json)
    actors = __get_persons_objs(actors)
    directors = __get_persons_objs(directors)
    return actors, directors


def __get_persons_objs(persons: list[dict[str, str | int]]) -> list[Person]:
    """
    Конвертирует информацию о людях в Person
    :param persons: список словарей с данными о людях
    :return: список из Person
    """
    return [
        Person(
            id=person_dict.pop("id"),
            photo=person_dict.pop("photo"),
            text=present_data(person_dict),
        )
        for person_dict in persons
    ]


def get_person_data_and_projects_id(json: dict) -> tuple[str, list[int]]:
    """
    Получает текст о человеке и id его других проектов
    :param json: данные из api
    :return: текст о человеке и список с id его других проектов
    """
    text, projects_id = PersonDataAPI.get_person_data_and_projects_id(json)
    return present_data(text), projects_id
