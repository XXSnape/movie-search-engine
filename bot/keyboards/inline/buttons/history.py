from aiogram.types import InlineKeyboardButton
from keyboards.inline.callback_factory.history_factory import (
    DeleteHistoryCbData,
    HistoryCbData,
    WatchedMovieCbData,
)
from utils.constants.output_for_user import DELETE_OUTPUT, HISTORY_OUTPUT
from utils.enums.history_data import SelectActionWithHistory, SelectIntervalToDelete
from utils.enums.items import SwitchItem


def get_btn_for_switch_watched_movie(
    watched_cb: WatchedMovieCbData, idx: int, switch: SwitchItem
) -> InlineKeyboardButton:
    """
    Обрабатывает кнопку для переключения фильма в истории

    :param watched_cb: WatchedMovieCbData
    :param idx: текущий индекс
    :param switch: SwitchItem
    :return: InlineKeyboardButton
    """
    watched_cb = watched_cb.model_copy()
    idx += 1 if switch == SwitchItem.NEXT else -1
    watched_cb.index = idx
    return InlineKeyboardButton(text=switch, callback_data=watched_cb.pack())


def get_buttons_for_history() -> list[InlineKeyboardButton]:
    """
    Возвращает кнопки для управления историей
    :return: список с InlineKeyboardButton
    """
    return [
        InlineKeyboardButton(
            text=f"Просмотреть историю{HISTORY_OUTPUT}",
            callback_data=HistoryCbData(options=SelectActionWithHistory.VIEW).pack(),
        ),
        InlineKeyboardButton(
            text=f"Удалить историю{DELETE_OUTPUT}",
            callback_data=HistoryCbData(options=SelectActionWithHistory.DELETE).pack(),
        ),
    ]


def get_buttons_for_delete_history() -> list[InlineKeyboardButton]:
    """
    Возвращает кнопки для удаления истории
    :return: список с InlineKeyboardButton
    """
    return [
        InlineKeyboardButton(
            text="Выбрать дату",
            callback_data=HistoryCbData(
                options=SelectActionWithHistory.DELETE_BY_DATE
            ).pack(),
        ),
        InlineKeyboardButton(
            text="За последнюю неделю",
            callback_data=DeleteHistoryCbData(
                options=SelectIntervalToDelete.WEEK
            ).pack(),
        ),
        InlineKeyboardButton(
            text="За последний месяц",
            callback_data=DeleteHistoryCbData(
                options=SelectIntervalToDelete.MONTH
            ).pack(),
        ),
        InlineKeyboardButton(
            text="За последний год",
            callback_data=DeleteHistoryCbData(
                options=SelectIntervalToDelete.YEAR
            ).pack(),
        ),
        InlineKeyboardButton(
            text="За все время",
            callback_data=DeleteHistoryCbData(
                options=SelectIntervalToDelete.ALL_TIME
            ).pack(),
        ),
    ]
