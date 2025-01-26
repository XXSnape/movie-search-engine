from enum import IntEnum, auto


class SelectActionWithRequest(IntEnum):
    """
    RESUME - сделать запрос снова
    SEND - продолжить запрос
    SWITCH - переключение запроса
    COMPLETE - завершить просмотр запросов
    DELETE - удалить запрос
    """

    RESUME = auto()
    SEND = auto()
    SWITCH = auto()
    COMPLETE = auto()
    DELETE = auto()
