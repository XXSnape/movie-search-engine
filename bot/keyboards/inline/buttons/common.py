from aiogram.types import InlineKeyboardButton
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from keyboards.inline.callback_factory.request_factory import RequestCbData
from utils.constants.output_for_user import CANCEL_OUTPUT, END_PREVIEW_OUTPUT
from utils.constants.router_keys import CANCEL_ROUTER
from utils.enums.commands import Commands
from utils.enums.items import SwitchItem
from utils.enums.movie_data import ViewingMovieDetails
from utils.enums.request_data import SelectActionWithRequest


def reset_full_data(callback_data: MovieBackCbData) -> None:
    """
    Возвращает MovieBackCbData параметры related_person_index и related_entity_index к базовому состоянию

    :param callback_data: MovieBackCbData
    :return: None
    """
    callback_data.related_person_index = 0
    callback_data.related_entity_index = 0


def reset_project_data(callback_data: MovieBackCbData) -> None:
    """
    Возвращает MovieBackCbData параметр  related_entity_index к базовому состоянию

    :param callback_data: MovieBackCbData
    :return: None
    """
    callback_data.related_entity_index = 0


def get_callback_with_reset_data(
    data_for_back: MovieBackCbData,
    new_option: ViewingMovieDetails,
    text: str,
    reset_func=reset_full_data,
) -> InlineKeyboardButton:
    """
    Обрабатывает полученную data_for_back

    :param data_for_back: MovieBackCbData
    :param new_option: новая стадия
    :param text: текст на кнопке
    :param reset_func: функция для возврата data_for_back к базовому состоянию
    :return: InlineKeyboardButton
    """
    data_for_back = data_for_back.model_copy()
    reset_func(data_for_back)
    data_for_back.options = new_option
    return InlineKeyboardButton(text=text, callback_data=data_for_back.pack())


def get_btn_for_switch_item(
    data_for_back: MovieBackCbData, idx: int, switch: SwitchItem
) -> InlineKeyboardButton:
    """
    Переключает контекст кнопки в зависимости от предыдущей стадии

    :param data_for_back: MovieBackCbData
    :param idx: индекс объекта
    :param switch: SwitchItem
    :return: InlineKeyboardButton
    """
    data_for_back = data_for_back.model_copy()
    idx += 1 if switch == SwitchItem.NEXT else -1
    if data_for_back.options == ViewingMovieDetails.MOVIES:
        data_for_back.index = idx
    elif data_for_back.options in (
        ViewingMovieDetails.ACTORS,
        ViewingMovieDetails.DIRECTORS,
    ):
        data_for_back.related_person_index = idx
    else:
        data_for_back.related_entity_index = idx
    return InlineKeyboardButton(text=switch, callback_data=data_for_back.pack())


def get_btn_for_end_watching_movies(ind: int) -> InlineKeyboardButton:
    """
    Получает кнопку для обработки завершения просмотра фильмов

    :param ind: индекс запроса
    :return: InlineKeyboardButton
    """
    return InlineKeyboardButton(
        text=END_PREVIEW_OUTPUT,
        callback_data=RequestCbData(
            index=ind, options=SelectActionWithRequest.COMPLETE
        ).pack(),
    )


def get_btn_for_cancel() -> InlineKeyboardButton:
    """
    Кнопка для отмены
    :return: InlineKeyboardButton
    """
    return InlineKeyboardButton(text=CANCEL_OUTPUT, callback_data=CANCEL_ROUTER)


def get_buttons_for_select_commands() -> list[InlineKeyboardButton]:
    """
    Кнопки с возможностями бота
    :return: список из InlineKeyboardButton
    """
    return [
        InlineKeyboardButton(text=command, callback_data=command)
        for command in Commands
    ]
