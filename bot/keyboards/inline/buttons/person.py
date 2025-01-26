from aiogram.types import InlineKeyboardButton
from keyboards.inline.buttons.common import (
    get_callback_with_reset_data,
    reset_project_data,
)
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from utils.constants.output_for_user import ACTOR_OUTPUT
from utils.enums.movie_data import ViewingMovieDetails


def get_btn_for_person_details(data_for_back: MovieBackCbData) -> InlineKeyboardButton:
    """
    Обрабатывает кнопку для получения подробной информации о человеке
    :param data_for_back: MovieBackCbData
    :return: InlineKeyboardButton
    """
    data_for_back = data_for_back.model_copy()
    options = {
        ViewingMovieDetails.ACTORS: ViewingMovieDetails.ACTOR_DETAILS,
        ViewingMovieDetails.DIRECTORS: ViewingMovieDetails.DIRECTOR_DETAILS,
    }
    data_for_back.options = options[data_for_back.options]
    return InlineKeyboardButton(text="Подробнее🧐", callback_data=data_for_back.pack())


def get_btn_for_back_to_persons(data_for_back: MovieBackCbData) -> InlineKeyboardButton:
    """
    Возвращает кнопку для возвращения к человеку

    :param data_for_back: MovieBackCbData
    :return: InlineKeyboardButton
    """
    option, text = _get_text_about_person(data_for_back.options)
    return get_callback_with_reset_data(data_for_back, option, text, reset_project_data)


def _get_text_about_person(
    current_option: ViewingMovieDetails,
) -> tuple[ViewingMovieDetails, str]:
    """
    Возвращает новую стадию и текст кнопки для возвращения к людям
    :param current_option: текущая стадия
    :return: ViewingMovieDetails и текст
    """
    data = ViewingMovieDetails
    actors = f"Вернуться к актерам{ACTOR_OUTPUT}"
    directors = f"Вернуться к режиссерам{ACTOR_OUTPUT}"
    texts = {
        data.ACTOR_DETAILS: (data.ACTORS, actors),
        data.ACTOR_PROJECTS: (data.ACTORS, actors),
        data.DIRECTOR_DETAILS: (data.DIRECTORS, directors),
        data.DIRECTOR_PROJECTS: (data.DIRECTORS, directors),
    }
    return texts[current_option]
