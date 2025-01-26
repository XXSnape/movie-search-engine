from aiogram.fsm.state import State, StatesGroup


class SearchMovieByTitleFSM(StatesGroup):
    """
    Состояния команды для поиска фильмов по названию
    """

    title = State()


class SearchMovieByDataFSM(StatesGroup):
    """
    Состояния для поиска фильмов по различным параметрам
    """

    sorting = State()
    genres = State()
    types = State()
    countries = State()
    years = State()
    statuses = State()
    networks = State()
    cinemas = State()
    reviews = State()
    collection = State()
    collection_cinemas = State()
