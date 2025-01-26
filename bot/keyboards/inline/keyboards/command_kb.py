from aiogram.types import InlineKeyboardMarkup
from keyboards.inline.buttons.common import (
    get_btn_for_cancel,
    get_buttons_for_select_commands,
)
from keyboards.inline.keyboards.mixins.generate_kb import GenerateInlineKeyboardMixin


class InlineKbForCommand(GenerateInlineKeyboardMixin):
    """
    Класс для генерации клавиатур, связанных с командами
    """

    @classmethod
    def get_kb_to_select_command(cls) -> InlineKeyboardMarkup:
        """
        Возвращает кнопки с доступными командами
        :return: InlineKeyboardMarkup
        """
        buttons = get_buttons_for_select_commands()
        return cls._generate_inline_kb(data_with_buttons=buttons, sizes=[2, 2, 1])

    @classmethod
    def get_kb_to_exit_command(cls):
        buttons = [get_btn_for_cancel()]
        return cls._generate_inline_kb(data_with_buttons=buttons)
