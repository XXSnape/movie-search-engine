from aiogram.fsm.context import FSMContext
from api.movie_search.movie_advanced_search import MovieAdvancedSearch
from api.movie_search.movie_cache import MovieCache
from api.movie_search.movie_mixins import MovieApiMixin
from api.utils import get_persons, get_projects
from cache.data_for_cache import MovieFromAnotherProjectCache
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from utils.constants.api_data import RATING_SORT, YEAR_SORT
from utils.enums.items import SortItem


class MovieRelatedSearch(MovieApiMixin):
    """
    Класс для отправки запросов на api для получения связанных фильмов
    """

    @classmethod
    async def get_related_projects_title_and_len(
        cls, attribute: str, callback_data: MovieBackCbData, cache: FSMContext
    ) -> tuple[MovieFromAnotherProjectCache, str, int]:
        """
        Получает информацию о связанных фильмах по атрибуту (похожие фильмы, продолжения)

        :param attribute: атрибут MovieBigInfoCache
        :param callback_data: MovieBackCbData
        :param cache: кэш с данными
        :return: MovieFromAnotherProjectCache, название фильма, количество фильмов в кэше
        """
        movie = await MovieCache.get_movie_by_id(
            movie_id=callback_data.movie_id, cache=cache
        )
        result = get_projects(
            getattr(movie, attribute), movie, callback_data.related_entity_index
        )
        if result:
            return result
        projects = await MovieAdvancedSearch.get_related_movies_by_ids(
            ids=getattr(movie, attribute),
            sort_field=YEAR_SORT,
            sort_type=SortItem.ASCEND,
            is_sequel=attribute == "sequels",
        )
        setattr(movie, attribute, projects)
        return get_projects(
            getattr(movie, attribute), movie, callback_data.related_entity_index
        )

    @classmethod
    async def get_person_project_title_and_len(
        cls, callback_data: MovieBackCbData, cache: FSMContext
    ) -> tuple[MovieFromAnotherProjectCache, str, int]:
        """
        Получает информацию о другом фильме человека

        :param callback_data: MovieBackCbData
        :param cache: кэш с данными
        :return: MovieFromAnotherProjectCache, название фильма, количество фильмов в кэше
        """
        movie = await MovieCache.get_movie_by_id(
            movie_id=callback_data.movie_id, cache=cache
        )
        person = get_persons(callback_data.options, movie)[
            callback_data.related_person_index
        ]
        projects = get_projects(
            person.projects, movie, callback_data.related_entity_index
        )
        if projects:
            return projects
        person.projects = await MovieAdvancedSearch.get_related_movies_by_ids(
            ids=person.projects, sort_field=RATING_SORT, sort_type=-1
        )
        return get_projects(person.projects, movie, callback_data.related_entity_index)
