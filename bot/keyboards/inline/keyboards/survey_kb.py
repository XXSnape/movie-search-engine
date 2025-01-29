from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from cache.get_data import get_data_from_cache
from keyboards.inline.buttons.common import get_btn_for_cancel
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from keyboards.inline.callback_factory.survey_factory import (
    CollectionCbData,
    MovieCbData,
)
from keyboards.inline.keyboards.mixins.generate_kb import GenerateInlineKeyboardMixin
from states.movie_search import SearchMovieByDataFSM
from utils.buttons.get_buttons import get_buttons_for_back_by_callback
from utils.constants.cache_keys import CALLBACK_DATA_CACHE
from utils.constants.output_for_user import (
    CANCEL_OUTPUT,
    COMPLETE_SELECTION_OUTPUT,
    GUARANTEED_ELEMENT,
    SUCCESSFULLY_OUTPUT,
)
from utils.constants.router_keys import ANY_PLATFORM_ROUTER, CANCEL_ROUTER, END_ROUTER
from utils.enums.items import SortType
from utils.survey_data import (
    API_CINEMAS,
    API_NETWORKS,
    RUSSIAN_COUNTRIES,
    RUSSIAN_GENRES,
    RUSSIAN_STATUSES,
    RUSSIAN_TYPES,
    RUSSIAN_TYPES_REVIEWS,
)
from utils.survey_data.collections import COLLECTIONS


class InlineKbForSurvey(GenerateInlineKeyboardMixin):
    """
    Класс для генерации клавиатур, связанных с опросами
    """

    @classmethod
    def __get_item(cls) -> dict[int, str]:
        """
        Возвращает словарь с символами для отображения пользователю
        :return: dict[int, str]
        """
        return {0: "", 1: SUCCESSFULLY_OUTPUT, 2: GUARANTEED_ELEMENT}

    @classmethod
    def __get_buttons_by_state(cls, state: State | None) -> list[list[str, str]]:
        """
        Генерирует список с данными для выбора по текущему состоянию
        :param state: State
        :return: список со списками с данными и индексом
        """
        states = {
            SearchMovieByDataFSM.genres: RUSSIAN_GENRES,
            SearchMovieByDataFSM.types: RUSSIAN_TYPES,
            SearchMovieByDataFSM.countries: RUSSIAN_COUNTRIES,
            SearchMovieByDataFSM.statuses: RUSSIAN_STATUSES,
            SearchMovieByDataFSM.cinemas: API_CINEMAS,
            SearchMovieByDataFSM.collection_cinemas: API_CINEMAS,
            SearchMovieByDataFSM.reviews: RUSSIAN_TYPES_REVIEWS,
            SearchMovieByDataFSM.networks: API_NETWORKS,
        }
        data = states[state]
        return [
            [type, MovieCbData(data=index).pack()] for index, type in enumerate(data)
        ]

    @classmethod
    def get_kb_to_select_buttons(
        cls, state: State, additional_buttons: list[InlineKeyboardButton] | tuple = ()
    ) -> tuple[InlineKeyboardMarkup, list[list[str, str]]]:
        """
        Генерирует клавиатуру для выбора элементов опроса

        :param state: State
        :param additional_buttons: список с дополнительными кнопками
        :return: InlineKeyboardMarkup и кнопки для сохранения в кэше
        """
        buttons = cls.__get_buttons_by_state(state)
        if state in (
            SearchMovieByDataFSM.cinemas,
            SearchMovieByDataFSM.collection_cinemas,
        ):
            buttons.append(["Любая платформа", ANY_PLATFORM_ROUTER])
        buttons.append([COMPLETE_SELECTION_OUTPUT, END_ROUTER])
        buttons.append([CANCEL_OUTPUT, CANCEL_ROUTER])
        return (
            cls._generate_inline_kb(
                data_with_buttons=additional_buttons, data_with_cb=buttons
            ),
            buttons,
        )

    @classmethod
    async def get_kb_with_modified_btn(
        cls,
        callback_data: MovieCbData,
        buttons: list[list[str, str]],
        cache: FSMContext,
    ) -> InlineKeyboardMarkup:
        """
        Изменяет клавиатуру после нажатия на элемент

        :param callback_data: MovieCbData
        :param buttons: кнопки
        :param cache: кэш с данными
        :return: InlineKeyboardMarkup
        """
        index = callback_data.data
        callback_data.num_clicks = (
            callback_data.num_clicks + 1
        ) % await cls.__get_divider(cache)
        record: str = buttons[index][0]
        if record[-1].isalpha():
            record = record + cls.__get_item()[callback_data.num_clicks]
        else:
            record = record[:-1] + cls.__get_item()[callback_data.num_clicks]
        buttons[index][1] = callback_data.pack()
        buttons[index][0] = record
        buttons_for_back = await cls.__get_buttons_to_back(cache)

        return cls._generate_inline_kb(
            data_with_buttons=buttons_for_back, data_with_cb=buttons
        )

    @classmethod
    def get_kb_with_collections_categories(cls) -> InlineKeyboardMarkup:
        """
        Генерирует клавиатуру с коллекциями
        :return: InlineKeyboardMarkup
        """
        buttons = [
            InlineKeyboardButton(
                text=category, callback_data=CollectionCbData(type=index).pack()
            )
            for index, category in enumerate(
                (
                    "Фильмы",
                    "Сериалы",
                    "Рекомендации онлайн-кинотеатров",
                    "Награды",
                    "Сборы",
                )
            )
        ]
        buttons.append(get_btn_for_cancel())
        return cls._generate_inline_kb(data_with_buttons=buttons)

    @classmethod
    def get_kb_to_select_collection(
        cls, collection_callback: CollectionCbData
    ) -> InlineKeyboardMarkup:
        """
        Генерирует клавиатуру для выбора коллекции

        :param collection_callback:CollectionCbData
        :return: InlineKeyboardMarkup
        """
        collection = COLLECTIONS[collection_callback.type]
        buttons = [
            InlineKeyboardButton(text=text, callback_data=slug)
            for slug, text in collection.items()
        ]
        buttons.append(get_btn_for_cancel())
        return cls._generate_inline_kb(data_with_buttons=buttons)

    @classmethod
    async def __get_divider(cls, cache: FSMContext) -> int:
        """
        Определяет, можно ли использовать элементы в сочетании друг с другом по состоянию
        :param cache: кэш с данными
        :return: int
        """
        current_state = await cache.get_state()
        if current_state in {
            "SearchMovieByDataFSM:reviews",
            "SearchMovieByDataFSM:networks",
            "SearchMovieByDataFSM:statuses",
        }:
            return 2
        return 3

    @classmethod
    async def __get_buttons_to_back(
        cls, state: FSMContext
    ) -> list[InlineKeyboardButton] | tuple:
        """
        Возвращает кнопки для перехода к фильмам при выборе отзыва
        :param state: кэш с данными
        :return: list[InlineKeyboardButton] или пустой tuple
        """
        cb: MovieBackCbData = await get_data_from_cache(
            CALLBACK_DATA_CACHE, cache=state
        )
        if cb:
            return await get_buttons_for_back_by_callback(cb, state)
        return ()

    @classmethod
    def get_buttons_to_select_sort_type(cls) -> InlineKeyboardMarkup:
        """
        Возвращает клавиатуру для выбора типа сортировки
        :return: InlineKeyboardMarkup
        """
        buttons = [
            InlineKeyboardButton(text="По рейтингу", callback_data=SortType.BY_RATING),
            InlineKeyboardButton(
                text="По году выхода в России", callback_data=SortType.BY_YEAR
            ),
            get_btn_for_cancel(),
        ]
        return cls._generate_inline_kb(data_with_buttons=buttons)
