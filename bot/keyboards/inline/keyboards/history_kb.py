from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from keyboards.inline.buttons.common import get_btn_for_cancel
from keyboards.inline.buttons.favorite import get_buttons_for_manage_favorite
from keyboards.inline.buttons.history import (
    get_btn_for_switch_watched_movie,
    get_buttons_for_delete_history,
    get_buttons_for_history,
)
from keyboards.inline.callback_factory.history_factory import WatchedMovieCbData
from keyboards.inline.keyboards.mixins.generate_kb import (
    ButtonsInCacheMixin,
    GenerateInlineKeyboardMixin,
    SwitchItemsMixin,
)


class InlineKbForHistory(
    GenerateInlineKeyboardMixin, SwitchItemsMixin, ButtonsInCacheMixin
):
    """
    Класс для генерации клавиатур, связанных с историей
    """

    @classmethod
    def get_kb_for_history(cls) -> InlineKeyboardMarkup:
        """
        Возвращает клавиатуру для управления историей
        :return: InlineKeyboardMarkup
        """
        buttons = get_buttons_for_history()
        buttons.append(get_btn_for_cancel())
        return cls._generate_inline_kb(data_with_buttons=buttons)

    @classmethod
    def get_kb_to_select_delete_options(cls) -> InlineKeyboardMarkup:
        """
        Возвращает клавиатуру для удаления истории
        :return: InlineKeyboardMarkup
        """
        buttons = get_buttons_for_delete_history()
        buttons.append(get_btn_for_cancel())
        return cls._generate_inline_kb(data_with_buttons=buttons)

    @classmethod
    async def get_kb_to_switch_watched_movie(
        cls,
        idx: int,
        length: int,
        movie_id: int,
        favorite_ids: list[int],
        cache: FSMContext,
        watched_cb: WatchedMovieCbData | None = None,
    ) -> InlineKeyboardMarkup:
        """
        Генерирует клавиатуру для переключения фильмов

        :param idx: текущий индекс
        :param length: количество фильмов
        :param movie_id: id фильма
        :param favorite_ids: id фильмов в избранном
        :param cache: кэш с данными
        :param watched_cb: WatchedMovieCbData или None
        :return: InlineKeyboardMarkup
        """
        if watched_cb is None:
            watched_cb = WatchedMovieCbData(index=idx)
        buttons = [
            get_buttons_for_manage_favorite(movie_id, favorite_ids),
            get_btn_for_cancel(),
        ]

        cls._add_buttons_for_switch_items(
            cb_data=watched_cb,
            buttons=buttons,
            idx=idx,
            length=length,
            generate_btn=get_btn_for_switch_watched_movie,
        )
        sizes = [1, 1, 2]
        await cls._add_button_data_to_cache(
            cache, buttons, favorite_index=0, sizes=sizes
        )
        return cls._generate_inline_kb(data_with_buttons=buttons, sizes=sizes)
