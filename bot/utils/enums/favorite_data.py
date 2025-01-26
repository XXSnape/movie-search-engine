from enum import IntEnum, auto


class SelectActionWithFavorite(IntEnum):
    """
    ADD - добавить в избранное
    DELETE - удалить из избранного
    """

    ADD = auto()
    DELETE = auto()
