from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from cache.get_data import get_data_from_cache
from database.models import HistoryModel
from keyboards.inline.callback_factory.history_factory import HistoryCbData
from keyboards.inline.keyboards.history_kb import InlineKbForHistory
from services.favorite import get_favorite_movies_by_user_id
from services.history import get_dates_and_max_date, get_history_by_date
from sqlalchemy.ext.asyncio import AsyncSession
from states.history import HistoryFsm
from utils.constants.cache_keys import (
    DATES_CACHE,
    FAVORITE_IDS_CACHE,
    MAX_DATE_CACHE,
    WATCHED_MOVIES_CACHE,
)
from utils.constants.output_for_user import (
    CANCEL_OUTPUT,
    REQUIRE_ACTION_OUTPUT,
    TODAY_OUTPUT,
)
from utils.enums.history_data import SelectActionWithHistory
from utils.tg.calendar import ExtendedSimpleCalendar
from utils.tg.process_photo import send_photo


async def handle_history(
    session: AsyncSession,
    callback: CallbackQuery,
    cache: FSMContext,
) -> None:
    """
    Обрабатывает команду history
    :param session: сессия для работы с базой
    :param callback: CallbackQuery
    :param cache: кэш с данными
    :return: None
    """
    await cache.clear()
    dates, max_date = await get_dates_and_max_date(
        session=session, user_id=callback.from_user.id
    )
    if not dates:
        await callback.answer(text="История пуста", show_alert=True)
        return
    await cache.update_data({DATES_CACHE: dates, MAX_DATE_CACHE: max_date})
    markup = InlineKbForHistory.get_kb_for_history()
    await callback.message.edit_text(text=REQUIRE_ACTION_OUTPUT, reply_markup=markup)


async def get_calendar(cache: FSMContext) -> ExtendedSimpleCalendar:
    """
    Возвращает календарь по датам из кэша
    :param cache: кэш с данными
    :return: ExtendedSimpleCalendar
    """
    dates = await get_data_from_cache(DATES_CACHE, cache=cache)
    return ExtendedSimpleCalendar(
        cancel_btn=CANCEL_OUTPUT,
        today_btn=TODAY_OUTPUT,
        show_alerts=True,
        available_dates=dates,
    )


async def get_calendar_and_max_date(
    cache: FSMContext, callback_data: HistoryCbData
) -> tuple[ExtendedSimpleCalendar, datetime]:
    """
    Возвращает календарь и максимально возможную дату
    :param cache: кэш с данными
    :param callback_data: HistoryCbData
    :return: tuple[ExtendedSimpleCalendar, datetime]
    """
    calendar = await get_calendar(cache)
    max_date = await get_data_from_cache(MAX_DATE_CACHE, cache=cache)
    new_state = (
        HistoryFsm.VIEW
        if callback_data.options == SelectActionWithHistory.VIEW
        else HistoryFsm.DELETE
    )
    await cache.set_state(new_state)
    return calendar, max_date


async def send_first_movie_from_history(
    session: AsyncSession,
    callback: CallbackQuery,
    cache: FSMContext,
    date: datetime,
    calendar: ExtendedSimpleCalendar,
) -> None:
    """
    Обрабатывает выбранную дату и отправляет первый фильм за этот день

    :param session: сессия для работы с базой
    :param callback: CallbackQuery
    :param cache: кэш с данными
    :param date: datetime
    :param calendar: ExtendedSimpleCalendar
    :return: None
    """
    watched_movies = await get_history_by_date(
        session=session, user_id=callback.from_user.id, date=date
    )
    if not watched_movies:
        await callback.answer("Нет истории за этот день", show_alert=True)
        await callback.message.edit_text(
            text="Выберете другую дату",
            reply_markup=await calendar.start_calendar(
                year=date.year, month=date.month
            ),
        )
        return
    start_movie: HistoryModel = watched_movies[0]
    favorite_ids = await get_favorite_movies_by_user_id(session, callback.from_user.id)
    markup = await InlineKbForHistory.get_kb_to_switch_watched_movie(
        idx=0,
        length=len(watched_movies),
        movie_id=start_movie.movie_id,
        favorite_ids=favorite_ids,
        cache=cache,
    )
    await cache.set_state(HistoryFsm.SWITCH)
    await cache.update_data(
        {WATCHED_MOVIES_CACHE: watched_movies, FAVORITE_IDS_CACHE: favorite_ids}
    )
    await callback.message.delete()
    await send_photo(
        message=callback.message,
        text=start_movie.text,
        photo=start_movie.url,
        markup=markup,
    )
