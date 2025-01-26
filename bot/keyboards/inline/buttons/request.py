from aiogram.types import InlineKeyboardButton
from keyboards.inline.callback_factory.request_factory import RequestCbData
from utils.constants.output_for_user import DELETE_OUTPUT
from utils.enums.items import SwitchItem
from utils.enums.request_data import SelectActionWithRequest


def get_btn_for_send_request(request_cb: RequestCbData) -> InlineKeyboardButton:
    """
    Обрабатывает кнопку для продолжения просмотра фильмов
    :param request_cb: RequestCbData
    :return: InlineKeyboardButton
    """
    request_cb = request_cb.model_copy()
    request_cb.options = SelectActionWithRequest.SEND
    return InlineKeyboardButton(
        text="Продолжить просмотр🔛", callback_data=request_cb.pack()
    )


def get_btn_for_resume_request(request_cb: RequestCbData) -> InlineKeyboardButton:
    """
    Обрабатывает кнопку для того, чтобы сделать запрос снова
    :param request_cb: RequestCbData
    :return: InlineKeyboardButton
    """
    request_cb = request_cb.model_copy()
    request_cb.options = SelectActionWithRequest.RESUME
    return InlineKeyboardButton(
        text="Сделать запрос снова♻", callback_data=request_cb.pack()
    )


def get_btn_for_delete_request(request_cb: RequestCbData) -> InlineKeyboardButton:
    """
    Обрабатывает кнопку для удаления запроса
    :param request_cb: RequestCbData
    :return: InlineKeyboardButton
    """
    request_cb = request_cb.model_copy()
    request_cb.options = SelectActionWithRequest.DELETE
    return InlineKeyboardButton(
        text=f"Удалить запрос{DELETE_OUTPUT}", callback_data=request_cb.pack()
    )


def get_btn_for_switch_request(
    request_cb: RequestCbData, idx: int, switch: SwitchItem
) -> InlineKeyboardButton:
    """
    Обрабатывает кнопку для переключения запросов
    :param request_cb: RequestCbData
    :param idx: текущий индекс
    :param switch: SwitchItem
    :return: InlineKeyboardButton
    """
    request_cb = request_cb.model_copy()
    idx += 1 if switch == SwitchItem.NEXT else -1
    request_cb.options = SelectActionWithRequest.SWITCH
    request_cb.index = idx
    return InlineKeyboardButton(text=switch, callback_data=request_cb.pack())
