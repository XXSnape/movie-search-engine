from aiogram.types import InlineKeyboardMarkup
from keyboards.inline.buttons.common import get_btn_for_cancel
from keyboards.inline.buttons.request import (
    get_btn_for_delete_request,
    get_btn_for_resume_request,
    get_btn_for_send_request,
    get_btn_for_switch_request,
)
from keyboards.inline.callback_factory.request_factory import RequestCbData
from keyboards.inline.keyboards.mixins.generate_kb import (
    GenerateInlineKeyboardMixin,
    SwitchItemsMixin,
)


class InlineKbForRequest(GenerateInlineKeyboardMixin, SwitchItemsMixin):
    """
    Класс для генерации клавиатур, связанных с запросами
    """

    @classmethod
    def get_kb_to_select_actions(
        cls, idx: int, length: int, request_cb: RequestCbData | None = None
    ) -> InlineKeyboardMarkup:
        """
        Генерирует клавиатуру для выбора действий с запросами
        :param idx: индекс запроса
        :param length: количество запросов
        :param request_cb: RequestCbData или None
        :return: InlineKeyboardMarkup
        """
        if request_cb is None:
            request_cb = RequestCbData(index=idx)
        buttons = [
            get_btn_for_send_request(request_cb),
            get_btn_for_resume_request(request_cb),
            get_btn_for_delete_request(request_cb),
            get_btn_for_cancel(),
        ]
        cls._add_buttons_for_switch_items(
            cb_data=request_cb,
            buttons=buttons,
            idx=idx,
            length=length,
            generate_btn=get_btn_for_switch_request,
        )
        return cls._generate_inline_kb(data_with_buttons=buttons, sizes=[1, 1, 1, 1, 2])
