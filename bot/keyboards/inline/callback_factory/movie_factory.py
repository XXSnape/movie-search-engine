from aiogram.filters.callback_data import CallbackData
from utils.enums.favorite_data import SelectActionWithFavorite
from utils.enums.movie_data import ViewingMovieDetails


class MovieBackCbData(CallbackData, prefix="back"):
    """
    Используется для сохранения информации о фильме, на котором остановился пользователь.

    movie_id: id фильма
    index: текущий индекс фильма
    related_person_index: индекс человека, связанного с фильмом
    related_entity_index: индекс связанной с фильмом сущности
    options: ViewingMovieDetails
    """

    movie_id: int
    index: int
    related_person_index: int = 0
    related_entity_index: int = 0
    options: ViewingMovieDetails = ViewingMovieDetails.MOVIES


class FavoriteMovieCbData(CallbackData, prefix="favorite"):
    movie_id: int
    options: SelectActionWithFavorite
