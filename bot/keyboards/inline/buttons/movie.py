from typing import Any

from aiogram.types import InlineKeyboardButton
from keyboards.inline.buttons.common import get_callback_with_reset_data
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from utils.enums.movie_data import ViewingMovieDetails


def get_btn_for_back_to_movies(data_for_back: MovieBackCbData) -> InlineKeyboardButton:
    """
    Возвращает кнопку для возвращения к фильмам
    :param data_for_back: MovieBackCbData
    :return: InlineKeyboardButton
    """
    return get_callback_with_reset_data(
        data_for_back, ViewingMovieDetails.MOVIES, "Вернуться к фильмам🎥"
    )


def get_btn_for_back_to_movie(
    data_for_back: MovieBackCbData, title: str
) -> InlineKeyboardButton:
    """
    Возвращает кнопку для возвращения к фильму

    :param data_for_back: MovieBackCbData
    :param title: название фильма
    :return: InlineKeyboardButton
    """
    return get_callback_with_reset_data(
        data_for_back,
        ViewingMovieDetails.MOVIE_DETAILS,
        f"Вернуться к «{title}»",
    )


def get_btn_for_movie_details(movie_id: int, idx: int) -> InlineKeyboardButton:
    """
    Возвращает кнопку для просмотра деталей фильма
    :param movie_id: id фильма
    :param idx: индекс фильма
    :return: InlineKeyboardButton
    """
    return InlineKeyboardButton(
        text="Подробнее🔎",
        callback_data=MovieBackCbData(
            movie_id=movie_id,
            index=idx,
            options=ViewingMovieDetails.MOVIE_DETAILS,
        ).pack(),
    )


def get_buttons_for_back_to_movies(
    data_for_back: MovieBackCbData, title: str
) -> list[InlineKeyboardButton]:
    """
    Собирает кнопки в список для возвращения к фильмам
    :param data_for_back: MovieBackCbData
    :param title: название текущего фильма
    :return: список с InlineKeyboardButton
    """
    return [
        get_btn_for_back_to_movies(data_for_back),
        get_btn_for_back_to_movie(data_for_back, title),
    ]


def get_obj_btn(
    data_for_back: MovieBackCbData,
    new_option: ViewingMovieDetails,
    text: str,
    obj: Any = True,
) -> InlineKeyboardButton | None:
    """
    Настраивает кнопку и возвращает ее в зависимости от объекта obj

    :param data_for_back: MovieBackCbData
    :param new_option: новая стадия
    :param text: текст кнопки
    :param obj: объекты для проверки
    :return: InlineKeyboardButton или None
    """
    data_for_back.options = new_option
    if obj:
        return InlineKeyboardButton(text=text, callback_data=data_for_back.pack())
