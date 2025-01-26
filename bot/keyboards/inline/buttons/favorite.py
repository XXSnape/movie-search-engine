from aiogram.types import InlineKeyboardButton
from keyboards.inline.callback_factory.movie_factory import FavoriteMovieCbData
from utils.constants.output_for_user import DELETE_OUTPUT, FAVORITE_OUTPUT
from utils.enums.favorite_data import SelectActionWithFavorite


def get_btn_for_add_to_favorite(movie_id: int) -> InlineKeyboardButton:
    """
    Обрабатывает кнопку для добавления в избранное
    :param movie_id: id фильма
    :return: InlineKeyboardButton
    """
    return InlineKeyboardButton(
        text=f"Добавить в Избранное{FAVORITE_OUTPUT}",
        callback_data=FavoriteMovieCbData(
            movie_id=movie_id, options=SelectActionWithFavorite.ADD
        ).pack(),
    )


def get_btn_for_delete_from_favorite(movie_id: int) -> InlineKeyboardButton:
    """
    Обрабатывает кнопку для удаления из избранного
    :param movie_id: id фильма
    :return: InlineKeyboardButton
    """
    return InlineKeyboardButton(
        text=f"Удалить из Избранного{DELETE_OUTPUT}",
        callback_data=FavoriteMovieCbData(
            movie_id=movie_id, options=SelectActionWithFavorite.DELETE
        ).pack(),
    )


def get_buttons_for_manage_favorite(
    movie_id: int, favorite_ids: list[int]
) -> InlineKeyboardButton:
    """
    Возвращает кнопку для управления избранным в зависимости от того, есть ли текущий фильм в избранном
    :param movie_id: id фильма
    :param favorite_ids: список с id фильмов в избранном
    :return: InlineKeyboardButton
    """
    if movie_id in favorite_ids:
        return get_btn_for_delete_from_favorite(movie_id)
    return get_btn_for_add_to_favorite(movie_id)
