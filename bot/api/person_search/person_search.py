from aiogram.fsm.context import FSMContext
from api.utils import get_persons
from cache.data_for_cache import MovieBigInfoCache, Person
from cache.get_data import get_data_from_cache
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData

from .person_mixins import PersonApiMixin
from .person_processing import get_person_data_and_projects_id


class PersonSearch(PersonApiMixin):
    """
    Класс для отправки запросов на api для получения информации о людях
    """

    @classmethod
    async def get_person_title_and_len(
        cls, callback_data: MovieBackCbData, cache: FSMContext
    ) -> tuple[Person, str, int]:
        """
        Получает информацию о человеке, название текущего фильма и количество всех людей
        :param callback_data: MovieBackCbData
        :param cache: кэш с данными
        :return: Person, название текущего фильма и количество всех людей
        """
        movie: MovieBigInfoCache = await get_data_from_cache(
            str(callback_data.movie_id), cache=cache
        )
        persons = get_persons(callback_data.options, movie)
        return persons[callback_data.related_person_index], movie.title, len(persons)

    @classmethod
    async def get_detail_person_and_title(
        cls, callback_data: MovieBackCbData, cache: FSMContext
    ) -> tuple[Person, str]:
        """
        Отправляет запрос на получение детальной информации о человеке

        :param callback_data: MovieBackCbData
        :param cache: кэш с данными
        :return: Person, название текущего фильма
        """
        movie: MovieBigInfoCache = await get_data_from_cache(
            str(callback_data.movie_id), cache=cache
        )
        person = get_persons(callback_data.options, movie)[
            callback_data.related_person_index
        ]
        if person.full_text is not None:
            return person, movie.title
        json_resp = await cls._make_request(url=person.id)
        text, projects = get_person_data_and_projects_id(json_resp)
        person.full_text = text
        person.projects = projects
        return person, movie.title
