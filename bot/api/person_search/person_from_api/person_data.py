from config.settings import settings
from utils.response_formats import get_pretty_date, join_by_sep
from utils.validators import get_value


class PersonDataAPI:
    """
    Класс с функциями, связанными с людьми, достающими данные из ответа api
    """

    @classmethod
    def get_actors_and_directors(cls, json: dict) -> tuple[
        list[dict[str, str | int]],
        list[dict[str, str | int]],
    ]:
        """
        Получает базовую информацию об актерах и режиссерах
        :param json: данные из api
        :return: 2 списка с актерами и режиссерами
        """
        actors = []
        directors = []
        for person in json.get("persons", ()):
            person_obj = {
                "Имя": person.get("name"),
                "Роль": person.get("description"),
                "id": person.get("id"),
                "photo": person.get("photo"),
            }
            if person.get("profession") == "актеры":
                actors.append(person_obj)
            elif person.get("profession") == "режиссеры":
                directors.append(person_obj)
        return (
            actors[: settings.API.NUMBER_PERSONS],
            directors[: settings.API.NUMBER_PERSONS],
        )

    @classmethod
    def get_person_data_and_projects_id(cls, json: dict) -> tuple[
        dict[str, int | str],
        list[int],
    ]:
        """
        Получает расширенную информацию о человеке и id его проектов

        :param json: данные из api
        :return: словарь с данными человека и список с id его проектов
        """
        projects = [
            movie["id"]
            for movie in json.get("movies", ())[: settings.API.NUMBER_PROJECTS]
        ]
        data = {
            "Имя": json.get("name"),
            "Рост": get_value("growth", json=json),
            "Возраст": json.get("age"),
            "Дата рождения": get_pretty_date(json.get("birthday")),
            "Дата смерти": get_pretty_date(json.get("death")),
            "Место Рождения": join_by_sep(
                (
                    place["value"]
                    for place in get_value("birthPlace", json=json, return_result=())
                ),
                sep=". ",
            ),
        }
        return data, projects
