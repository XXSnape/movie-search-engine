from datetime import datetime, timedelta
from typing import Iterable

from aiogram.fsm.context import FSMContext
from cache.get_data import get_data_from_cache
from database.models import HistoryModel
from database.repository.history import HistoryRepository
from keyboards.inline.callback_factory.history_factory import DeleteHistoryCbData
from sqlalchemy.ext.asyncio import AsyncSession
from utils.constants.cache_keys import MAX_DATE_CACHE
from utils.enums.history_data import SelectIntervalToDelete
from utils.response_formats import build_text
from utils.response_formats.pretty_response import get_russian_date


async def write_history(
    session: AsyncSession, user_id: int, movie_id: int, text: str, url: str
) -> None:
    """
    Пишет историю в базу

    :param session: сессия для работы с базой
    :param user_id: id пользователя
    :param movie_id: id фильма
    :param text: текст
    :param url: url фильма
    :return: None
    """
    await HistoryRepository.create_object(
        session=session,
        data={"user_tg_id": user_id, "movie_id": movie_id, "text": text, "url": url},
    )


async def get_history_by_date(
    session: AsyncSession, user_id: int, date: datetime
) -> Iterable[HistoryModel]:
    """
    Получает историю по дате

    :param session: сессия для работы с базой
    :param user_id: id пользователя
    :param date: дата
    :return: Iterable[HistoryModel]
    """
    movies: Iterable[HistoryModel] = await HistoryRepository.get_objects_by_params(
        session=session, data={"user_tg_id": user_id, "date": date}
    )
    pretty_date = build_text(
        f"Дата просмотра: {get_russian_date(date, is_time_displayed=False)}"
    )
    for movie in movies:
        movie.text = (
            f"{pretty_date}\n\n{movie.text}"  # добавление атрибута text HistoryModel
        )
    return movies


async def delete_history_by_date(
    session: AsyncSession, user_id: int, date: datetime
) -> None:
    """
    Удаляет историю по дате

    :param session: сессия для работы с базой
    :param user_id: id пользователя
    :param date: дата
    :return: None
    """
    await HistoryRepository.delete_object_by_params(
        session=session, data={"user_tg_id": user_id, "date": date}
    )


async def delete_history_by_interval(
    session: AsyncSession,
    user_id: int,
    callback_data: DeleteHistoryCbData,
    cache: FSMContext,
) -> None:
    """
    Удаляет историю по интервалу
    :param session: сессия для работы с базой
    :param user_id: id пользователя
    :param callback_data: DeleteHistoryCbData
    :param cache: FSMContext
    :return: None
    """
    max_date = await get_data_from_cache(MAX_DATE_CACHE, cache=cache)
    start_deleting_date = None
    if callback_data.options == SelectIntervalToDelete.WEEK:
        start_deleting_date = max_date - timedelta(weeks=1)
    elif callback_data.options == SelectIntervalToDelete.MONTH:
        start_deleting_date = datetime(year=max_date.year, month=max_date.month, day=1)
    elif callback_data.options == SelectIntervalToDelete.YEAR:
        start_deleting_date = datetime(year=max_date.year, month=1, day=1)
    if start_deleting_date is None:
        await HistoryRepository.delete_object_by_params(
            session=session, data={"user_tg_id": user_id}
        )
        return
    await HistoryRepository.delete_history_by_interval(
        session=session,
        user_id=user_id,
        start_date=start_deleting_date,
        last_date=max_date,
    )
    await cache.clear()


async def get_dates_and_max_date(
    session: AsyncSession, user_id: int
) -> tuple[set[datetime], datetime | None]:
    """
    Получает уникальные даты и максимальную дату из базы
    :param session: сессия для работы с базой
    :param user_id: id пользователя
    :return: tuple[set[datetime], datetime | None]
    """
    dates = {
        datetime(date.year, date.month, date.day)
        for date in await HistoryRepository.get_uniq_dates(
            session=session, user_id=user_id
        )
    }
    if dates:
        return dates, max(dates)
    return dates, None
