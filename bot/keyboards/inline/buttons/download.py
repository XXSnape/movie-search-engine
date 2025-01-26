from aiogram.types import InlineKeyboardButton
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from utils.enums.movie_data import ViewingMovieDetails


def get_btn_for_download(
    data_for_back: MovieBackCbData, type_download: ViewingMovieDetails
) -> InlineKeyboardButton:
    """
    Обрабатывает кнопку для подгрузки фильмов

    :param data_for_back: MovieBackCbData
    :param type_download: тип подгрузки
    :return: InlineKeyboardButton
    """
    data_for_back = data_for_back.model_copy()
    data_for_back.options = type_download
    return InlineKeyboardButton(
        text="Загрузить еще", callback_data=data_for_back.pack()
    )
