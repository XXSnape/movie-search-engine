from aiogram.types import InlineKeyboardMarkup
from keyboards.inline.buttons.common import get_btn_for_end_watching_movies
from keyboards.inline.buttons.movie import get_buttons_for_back_to_movies, get_obj_btn
from keyboards.inline.buttons.person import (
    get_btn_for_back_to_persons,
    get_btn_for_person_details,
)
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from keyboards.inline.keyboards.mixins.generate_kb import (
    GenerateInlineKeyboardMixin,
    SwitchItemsMixin,
)
from utils.enums.movie_data import ViewingMovieDetails


class InlineKbForPerson(GenerateInlineKeyboardMixin, SwitchItemsMixin):
    """
    Класс для генерации клавиатур, связанных с людьми
    """

    @classmethod
    def get_kb_to_switch_persons_and_view_details(
        cls, data_for_back: MovieBackCbData, title: str, length: int
    ) -> InlineKeyboardMarkup:
        """
        Генерирует клавиатуру для переключения людей
        :param data_for_back: MovieBackCbData
        :param title: названия фильма, связанного с человеком
        :param length: количество людей
        :return: InlineKeyboardMarkup
        """
        idx = data_for_back.related_person_index
        buttons = get_buttons_for_back_to_movies(data_for_back, title)
        buttons.append(get_btn_for_person_details(data_for_back))
        cls._add_buttons_for_switch_items(
            data_for_back, buttons=buttons, idx=idx, length=length
        )
        buttons.append(get_btn_for_end_watching_movies(data_for_back.index))
        sizes = [1, 1, 1, 2, 1] if len(buttons) == 6 else [1]
        return cls._generate_inline_kb(data_with_buttons=buttons, sizes=sizes)

    @classmethod
    def get_kb_for_back_to_persons_and_view_other_projects(
        cls, data_for_back: MovieBackCbData, projects: list[int], title: str
    ) -> InlineKeyboardMarkup:
        """
        Генерирует клавиатуру для возвращения к людям и просмотра других проектов
        :param data_for_back: MovieBackCbData
        :param projects: список с id проектов
        :param title: названия фильма, связанного с человеком
        :return: InlineKeyboardMarkup
        """
        buttons = get_buttons_for_back_to_movies(data_for_back, title)
        buttons.append(get_btn_for_back_to_persons(data_for_back))
        options = {
            ViewingMovieDetails.ACTOR_DETAILS: ViewingMovieDetails.ACTOR_PROJECTS,
            ViewingMovieDetails.DIRECTOR_DETAILS: ViewingMovieDetails.DIRECTOR_PROJECTS,
        }
        option = options[data_for_back.options]
        buttons.append(
            get_obj_btn(
                data_for_back,
                option,
                "Другие проекты🗂️",
                projects,
            )
        )
        buttons.append(get_btn_for_end_watching_movies(data_for_back.index))
        return cls._generate_inline_kb(data_with_buttons=buttons)
