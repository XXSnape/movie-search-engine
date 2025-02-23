from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from cache.data_for_cache import MovieBigInfoCache
from cache.get_data import get_data_from_cache
from keyboards.inline.buttons.common import get_btn_for_end_watching_movies
from keyboards.inline.buttons.download import get_btn_for_download
from keyboards.inline.buttons.favorite import get_buttons_for_manage_favorite
from keyboards.inline.buttons.movie import (
    get_btn_for_back_to_movies,
    get_btn_for_movie_details,
    get_buttons_for_back_to_movies,
    get_obj_btn,
)
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from keyboards.inline.keyboards.mixins.generate_kb import (
    ButtonsInCacheMixin,
    GenerateInlineKeyboardMixin,
    SwitchItemsMixin,
)
from utils.constants.cache_keys import (
    COMMAND_CACHE,
    FAVORITE_IDS_CACHE,
    MAX_PAGE_CACHE,
    MIN_PAGE_CACHE,
    PARAMS_CACHE,
)
from utils.constants.output_for_user import ACTOR_OUTPUT, CINEMA_OUTPUT, DIRECTOR_OUTPUT
from utils.enums.commands import Commands
from utils.enums.movie_data import ViewingMovieDetails


class InlineKbForMovie(
    GenerateInlineKeyboardMixin, SwitchItemsMixin, ButtonsInCacheMixin
):
    """
    Класс для генерации клавиатур, связанных с фильмами
    """

    @classmethod
    async def get_kb_to_switch_movie_and_view_details(
        cls, movie_id: int, idx: int, length: int, cache: FSMContext
    ) -> InlineKeyboardMarkup:
        """
        Генерирует клавиатуру для переключения фильмов
        :param movie_id: id фильма
        :param idx: индекс фильма
        :param length: количество фильмов
        :param cache: кэш с данными
        :return: InlineKeyboardMarkup
        """
        data = await cache.get_data()
        buttons = [
            get_btn_for_movie_details(movie_id, idx),
            get_buttons_for_manage_favorite(movie_id, data[FAVORITE_IDS_CACHE]),
        ]
        cb = MovieBackCbData(movie_id=movie_id, index=idx)
        num_buttons = cls._add_buttons_for_switch_items(
            cb, buttons=buttons, idx=idx, length=length
        )
        if num_buttons != 2:
            sizes = [1]
        else:
            sizes = [1, 1, 2, 1]
        cls.__add_btn_to_download(cb, buttons, num_buttons, data, idx, length)
        buttons.append(get_btn_for_end_watching_movies(idx))
        await cls._add_button_data_to_cache(
            cache, buttons, favorite_index=1, sizes=sizes
        )
        return cls._generate_inline_kb(data_with_buttons=buttons, sizes=sizes)

    @classmethod
    async def get_kb_for_movie_details(
        cls,
        data_for_back: MovieBackCbData,
        movie: MovieBigInfoCache,
        cache: FSMContext,
    ) -> InlineKeyboardMarkup:
        """
        Генерирует клавиатуру для просмотра деталей фильма

        :param data_for_back: MovieBackCbData
        :param movie: MovieBigInfoCache
        :param cache: кэш с данными
        :return: InlineKeyboardMarkup
        """
        data = ViewingMovieDetails
        favorite_ids = await get_data_from_cache(FAVORITE_IDS_CACHE, cache=cache)
        buttons = [
            get_btn_for_back_to_movies(data_for_back),
            get_obj_btn(
                data_for_back,
                data.PICTURES,
                "Кадры из фильма📸",
            ),
            get_obj_btn(
                data_for_back,
                data.WATCH,
                f"Где посмотреть?{CINEMA_OUTPUT}",
                movie.watchability,
            ),
            get_obj_btn(
                data_for_back, data.ACTORS, f"Актеры{ACTOR_OUTPUT}", movie.actors
            ),
            get_obj_btn(
                data_for_back,
                data.DIRECTORS,
                f"Режиссеры{DIRECTOR_OUTPUT}",
                movie.directors,
            ),
            get_obj_btn(
                data_for_back, data.SEQUELS, "Продолжения и приквелы🔄", movie.sequels
            ),
            get_obj_btn(
                data_for_back,
                data.SELECT_REVIEWS,
                "Отзывы📝",
            ),
            get_obj_btn(
                data_for_back,
                data.SIMILAR_PROJECTS,
                "Похожие фильмы🪞",
                movie.similar_projects,
            ),
            get_buttons_for_manage_favorite(
                data_for_back.movie_id, favorite_ids=favorite_ids
            ),
            get_btn_for_end_watching_movies(data_for_back.index),
        ]
        await cls._add_button_data_to_cache(
            cache, buttons, favorite_index=-2, sizes=[1]
        )
        return cls._generate_inline_kb(
            data_with_buttons=buttons,
        )

    @classmethod
    def get_kb_for_cinemas(
        cls, data_for_back: MovieBackCbData, movie: MovieBigInfoCache
    ) -> InlineKeyboardMarkup:
        """
        Генерирует клавиатуру для просмотра онлайн-кинотеатров

        :param data_for_back: MovieBackCbData
        :param movie: MovieBigInfoCache
        :return: InlineKeyboardMarkup
        """
        buttons = get_buttons_for_back_to_movies(data_for_back, movie.title)
        buttons.append(get_btn_for_end_watching_movies(data_for_back.index))
        return cls._generate_inline_kb(
            data_with_url=movie.watchability, data_with_buttons=buttons
        )

    @classmethod
    def __add_btn_to_download(
        cls,
        cb: MovieBackCbData,
        buttons: list,
        num_buttons: int,
        data: dict,
        idx: int,
        length: int,
    ) -> None:
        """
        Добавляет кнопки для подгрузки фильмов

        :param cb: MovieBackCbData
        :param buttons: список кнопок
        :param num_buttons: количество кнопок для переключения
        :param data: данные кэша
        :param idx: текущий индекс
        :param length: количество фильмов
        :return: None
        """
        if num_buttons != 2 and data[COMMAND_CACHE] != Commands.FAVORITE:
            current_page = data[PARAMS_CACHE]["page"]
            max_page = data[MAX_PAGE_CACHE]
            min_page = data[MIN_PAGE_CACHE]
            if idx == 0 and min_page != 1:
                buttons.append(
                    get_btn_for_download(cb, ViewingMovieDetails.DOWNLOAD_PREVIOUS)
                )
            elif current_page != max_page and idx == length - 1:
                buttons.append(
                    get_btn_for_download(cb, ViewingMovieDetails.DOWNLOAD_FOLLOWING)
                )
