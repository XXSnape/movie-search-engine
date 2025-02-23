from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from cache.get_data import get_watched_movie_len_and_favorite_ids
from keyboards.inline.callback_factory.history_factory import WatchedMovieCbData
from keyboards.inline.keyboards.history_kb import InlineKbForHistory
from states.history import HistoryFsm
from utils.tg.process_photo import edit_photo

router = Router()


@router.callback_query(HistoryFsm.SWITCH, WatchedMovieCbData.filter())
async def handle_sending_history(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: WatchedMovieCbData,
) -> None:
    """
    Переключает фильм из истории
    :param callback: CallbackQuery
    :param state: FSMContext
    :param callback_data: WatchedMovieCbData
    :return: None
    """
    movie, length, favorite_ids = await get_watched_movie_len_and_favorite_ids(
        idx=callback_data.index, cache=state
    )
    markup = await InlineKbForHistory.get_kb_to_switch_watched_movie(
        idx=callback_data.index,
        length=length,
        movie_id=movie.movie_id,
        favorite_ids=favorite_ids,
        cache=state,
    )
    await edit_photo(callback=callback, text=movie.text, photo=movie.url, markup=markup)
