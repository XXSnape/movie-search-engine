from enum import IntEnum, auto


class SelectActionWithHistory(IntEnum):
    """
    VIEW - просмотреть историю
    DELETE - удалить историю по интервалу
    DELETE_BY_DATE - удалить историю по дате
    """

    VIEW = auto()
    DELETE = auto()
    DELETE_BY_DATE = auto()


class SelectIntervalToDelete(IntEnum):
    WEEK = auto()
    MONTH = auto()
    YEAR = auto()
    ALL_TIME = auto()
