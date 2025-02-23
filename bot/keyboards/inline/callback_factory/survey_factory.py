from aiogram.filters.callback_data import CallbackData


class MovieCbData(CallbackData, prefix="data"):
    """
    data: индекс кнопки в списке со всеми кнопками
    num_clicks: количество кликов по кнопке
    """

    data: int
    num_clicks: int = 0


class CollectionCbData(CallbackData, prefix="collection"):
    """
    type: тип коллекции
    """

    type: int
