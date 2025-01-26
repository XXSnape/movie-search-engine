from enum import IntEnum, StrEnum


class SwitchItem(StrEnum):
    """
    NEXT - текст для переключения следующего элемента
    PREV - текст для переключения предыдущего элемента
    """

    NEXT = "➡️"
    PREV = "⬅️"


class SortItem(IntEnum):
    """
    DESCEND - сортировка ппо убыванию
    ASCEND - сортировка по возрастанию
    """

    DESCEND = -1
    ASCEND = 1


class TypeSelection(IntEnum):
    """
    CLASSIC_CHOICE - стандартный выбор элемента в опросе
    COMBINED_CHOICE - выбор элемента, который однозначно будет в результате с другими
    """

    CLASSIC_CHOICE = 1
    COMBINED_CHOICE = 2


class SortType(IntEnum):
    """
    BY_RATING - сортировка по рейтингу
    BY_YEAR - сортировка по году выпуска
    """

    BY_RATING = 0
    BY_YEAR = 1
