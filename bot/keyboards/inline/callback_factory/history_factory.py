from aiogram.filters.callback_data import CallbackData
from utils.enums.history_data import SelectActionWithHistory, SelectIntervalToDelete


class HistoryCbData(CallbackData, prefix="history"):
    """
    Действия с историей
    """

    options: SelectActionWithHistory


class DeleteHistoryCbData(CallbackData, prefix="delete_history"):
    """
    Действия с удалением истории
    """

    options: SelectIntervalToDelete


class WatchedMovieCbData(CallbackData, prefix="watched"):
    """
    index: текущий индекс
    """

    index: int
