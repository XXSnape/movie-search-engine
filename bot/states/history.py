from aiogram.fsm.state import State, StatesGroup


class HistoryFsm(StatesGroup):
    """
    Состояния для команды history
    """

    VIEW = State()
    DELETE = State()
    SWITCH = State()
