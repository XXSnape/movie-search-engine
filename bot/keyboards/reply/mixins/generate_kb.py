from collections.abc import Iterable

from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class GenerateReplyKeyboardMixin:
    """
    Миксин для генерации reply-клавиатур
    """

    @classmethod
    def _generate_reply_kb(
        cls,
        *texts,
        input_field_placeholder="Доступные действия:",
        sizes: Iterable[int] = (1,),
    ) -> ReplyKeyboardMarkup:
        """
        Генерирует клавиатуру

        :param texts: тексты для кнопок
        :param input_field_placeholder: текст в строке ввода пользователя
        :param sizes: Расположение кнопок
        :return: ReplyKeyboardMarkup
        """
        builder = ReplyKeyboardBuilder()
        for text in texts:
            text: str
            builder.button(text=text)
        builder.adjust(*sizes)
        return builder.as_markup(
            input_field_placeholder=input_field_placeholder,
            resize_keyboard=True,
            one_time_keyboard=True,
        )
