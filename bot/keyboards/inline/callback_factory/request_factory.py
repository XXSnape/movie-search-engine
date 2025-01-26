from aiogram.filters.callback_data import CallbackData
from utils.enums.request_data import SelectActionWithRequest


class RequestCbData(CallbackData, prefix="request"):
    """
    index: текущий индекс запроса
    options: SelectActionWithRequest
    """

    index: int
    options: SelectActionWithRequest = SelectActionWithRequest.SEND
