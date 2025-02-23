from aiogram.types import InlineKeyboardMarkup
from keyboards.inline.buttons.favorite import (
    get_btn_for_add_to_favorite,
    get_btn_for_delete_from_favorite,
)
from keyboards.inline.keyboards.mixins.generate_kb import GenerateInlineKeyboardMixin


class InlineKbForFavorite(GenerateInlineKeyboardMixin):
    """
    Класс для генерации клавиатур, связанных с избранным
    """

    @classmethod
    def replace_addition_with_deletion(
        cls, all_buttons: list, sizes: list[int], favorite_index: int, movie_id: int
    ) -> InlineKeyboardMarkup:
        """
        Заменяет кнопку добавления в избранное на удаление
        :param all_buttons: список с кнопками
        :param sizes: расположение кнопок
        :param favorite_index: текущий индекс фильма в избранном
        :param movie_id: id фильма
        :return: InlineKeyboardMarkup
        """
        data_with_buttons, data_with_url = cls._get_data_from_buttons(all_buttons)
        data_with_buttons[favorite_index] = get_btn_for_delete_from_favorite(
            movie_id=movie_id
        )
        return cls._generate_inline_kb(
            data_with_url=data_with_url,
            data_with_buttons=data_with_buttons,
            sizes=sizes,
        )

    @classmethod
    def replace_deletion_with_addition(
        cls, all_buttons: list, sizes: list[int], favorite_index: int, movie_id: int
    ):
        """
        Заменяет кнопку удаления из избранного на добавление
        :param all_buttons: список с кнопками
        :param sizes: расположение кнопок
        :param favorite_index: текущий индекс фильма в избранном
        :param movie_id: id фильма
        :return: InlineKeyboardMarkup
        """
        data_with_buttons, data_with_url = cls._get_data_from_buttons(all_buttons)
        data_with_buttons[favorite_index] = get_btn_for_add_to_favorite(
            movie_id=movie_id
        )
        return cls._generate_inline_kb(
            data_with_url=data_with_url,
            data_with_buttons=data_with_buttons,
            sizes=sizes,
        )

    @classmethod
    def _get_data_from_buttons(cls, all_buttons: list) -> tuple[list, list]:
        """
        Разделяет на списки с InlineKeyboardButton и url
        :param all_buttons: кнопки
        :return: список с кнопками, список с url
        """
        data_with_buttons = []
        data_with_url = []
        for data in all_buttons:
            if isinstance(data, list):
                data_with_url.append(data)
            else:
                data_with_buttons.append(data)
        return data_with_buttons, data_with_url
