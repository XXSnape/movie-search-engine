from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards.inline.keyboards.request_kb import InlineKbForRequest
from services.favorite import get_favorite_movies_by_user_id
from services.request import get_requests
from sqlalchemy.ext.asyncio import AsyncSession
from utils.constants.cache_keys import FAVORITE_IDS_CACHE, REQUESTS_CACHE


async def handle_requests(
    session: AsyncSession, callback: CallbackQuery, cache: FSMContext
) -> None:
    """
    Обрабатывает команду requests
    :param session: сессия для работы с базой
    :param callback: CallbackQuery
    :param cache: кэш по работе с базой
    :return: None
    """
    await cache.clear()
    favorite_ids = await get_favorite_movies_by_user_id(
        session=session, user_id=callback.from_user.id
    )
    requests = await get_requests(session=session, user_id=callback.from_user.id)
    if not requests:
        await callback.answer(
            "Нет запросов",
            show_alert=True,
        )
        return
    await cache.update_data(
        {REQUESTS_CACHE: requests, FAVORITE_IDS_CACHE: favorite_ids}
    )
    first_request = requests[0]
    markup = InlineKbForRequest.get_kb_to_select_actions(idx=0, length=len(requests))
    await callback.message.edit_text(text=first_request.text, reply_markup=markup)
