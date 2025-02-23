from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from cache.get_data import get_data_from_cache
from keyboards.inline.buttons.common import get_btn_for_end_watching_movies
from keyboards.inline.buttons.favorite import get_buttons_for_manage_favorite
from keyboards.inline.buttons.movie import get_buttons_for_back_to_movies
from keyboards.inline.buttons.person import get_btn_for_back_to_persons
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from keyboards.inline.keyboards.mixins.generate_kb import (
    ButtonsInCacheMixin,
    GenerateInlineKeyboardMixin,
    SwitchItemsMixin,
)
from utils.constants.cache_keys import FAVORITE_IDS_CACHE
from utils.enums.movie_data import ViewingMovieDetails


class InlineKbForProject(
    GenerateInlineKeyboardMixin, SwitchItemsMixin, ButtonsInCacheMixin
):
    """
    Класс для генерации клавиатур, связанных со связанными проектами
    """

    @classmethod
    async def get_kb_to_switch_entities(
        cls,
        data_for_back: MovieBackCbData,
        title: str,
        length: int,
        movie_id: int,
        cache: FSMContext,
        cinemas: list[list[str, str]] | None = None,
    ) -> InlineKeyboardMarkup:
        """
        Генерирует клавиатуру для переключения различных сущностей
        :param data_for_back: MovieBackCbData
        :param title: название фильма, связанного с проектами
        :param length: количество проектов
        :param movie_id: id фильма
        :param cache: кэш с данными
        :param cinemas: онлайн кинотеатры
        :return: InlineKeyboardMarkup
        """
        cinemas = [] if cinemas is None else cinemas
        idx = data_for_back.related_entity_index
        buttons = get_buttons_for_back_to_movies(data_for_back, title)
        if data_for_back.options in (
            ViewingMovieDetails.DIRECTOR_PROJECTS,
            ViewingMovieDetails.ACTOR_PROJECTS,
        ):
            buttons.append(get_btn_for_back_to_persons(data_for_back))
        buttons.append(
            get_buttons_for_manage_favorite(
                movie_id=movie_id,
                favorite_ids=await get_data_from_cache(FAVORITE_IDS_CACHE, cache=cache),
            )
        )
        buttons.append(get_btn_for_end_watching_movies(data_for_back.index))
        favorite_index = len(buttons) - 2
        num_buttons = cls._add_buttons_for_switch_items(
            data_for_back, buttons=buttons, idx=idx, length=length
        )
        sizes = [*[1] * (len(buttons) - num_buttons), num_buttons, 3]
        if 0 in sizes:
            sizes.remove(0)
        await cls._add_button_data_to_cache(
            cache, buttons=buttons + cinemas, favorite_index=favorite_index, sizes=sizes
        )
        return cls._generate_inline_kb(
            data_with_url=cinemas, data_with_buttons=buttons, sizes=sizes
        )
