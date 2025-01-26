from collections.abc import Callable
from typing import Iterable

from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.inline.buttons.common import get_btn_for_switch_item
from keyboards.inline.callback_factory.history_factory import WatchedMovieCbData
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from keyboards.inline.callback_factory.request_factory import RequestCbData
from utils.constants.cache_keys import (
    BUTTONS_KB_CACHE,
    FAVORITE_INDEX_CACHE,
    KEYBOARD_CACHE,
    SIZES_CACHE,
)
from utils.enums.items import SwitchItem


class GenerateInlineKeyboardMixin:
    """
    Миксин для генерации inline-клавиатур
    """

    @classmethod
    def _generate_inline_kb(
        cls,
        *,
        data_with_url=(),
        data_with_buttons=(),
        data_with_cb=(),
        sizes: Iterable[int] = (1,),
    ) -> InlineKeyboardMarkup:
        """
        Генерирует клавиатуру по различным данным
        :param data_with_url: итерируемый объект с названием и url
        :param data_with_buttons: итерируемый объект с готовыми кнопками
        :param data_with_cb: итерируемый объект с текстом и данными
        :param sizes: расположение кнопок
        :return: InlineKeyboardMarkup
        """
        builder = InlineKeyboardBuilder()
        for data in data_with_buttons:
            if data:
                builder.add(data)
        for data in data_with_url:
            builder.button(text=data[0], url=data[1])

        for data in data_with_cb:
            builder.button(text=data[0], callback_data=data[1])
        builder.adjust(*sizes)
        return builder.as_markup()


class SwitchItemsMixin:
    """Миксин для переключения сущностей с помощью кнопок"""

    @classmethod
    def _add_buttons_for_switch_items(
        cls,
        cb_data: MovieBackCbData | WatchedMovieCbData | RequestCbData,
        buttons: list,
        idx: int,
        length: int,
        generate_btn: Callable = get_btn_for_switch_item,
    ) -> int:
        """
        Генерирует кнопки для переключения объектов
        :param cb_data: MovieBackCbData | WatchedMovieCbData | RequestCbData
        :param buttons: список с кнопками
        :param idx: текущий индекс
        :param length: количество объектов
        :param generate_btn: функция для генерации кнопки
        :return: количество добавленных кнопок
        """
        num_buttons = 0
        if idx > 0:
            buttons.append(generate_btn(cb_data, idx, SwitchItem.PREV))
            num_buttons += 1
        if idx < length - 1:
            buttons.append(generate_btn(cb_data, idx, SwitchItem.NEXT))
            num_buttons += 1
        return num_buttons


class ButtonsInCacheMixin:
    """Миксин для сохранения данных о текущей клавиатуре в кэш"""

    @classmethod
    async def _add_button_data_to_cache(
        cls,
        cache: FSMContext,
        buttons: list[InlineKeyboardButton],
        favorite_index: int,
        sizes: list[int],
    ) -> None:
        """
        Сохраняет клавиатуру в кэш
        :param cache: кэш с данными
        :param buttons: список с кнопками
        :param favorite_index: текущий индекс фильма в избранном
        :param sizes: расположение кнопок
        :return: None
        """
        keyboard = {
            BUTTONS_KB_CACHE: buttons,
            FAVORITE_INDEX_CACHE: favorite_index,
            SIZES_CACHE: sizes,
        }
        await cache.update_data({KEYBOARD_CACHE: keyboard})
