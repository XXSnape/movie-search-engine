from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from utils.enums.commands import Commands
from utils.tg.router_assistants.favorite import handle_favorite

router = Router(name=__name__)


@router.callback_query(F.data == Commands.FAVORITE)
async def handle_favorite_movies(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    """
    Обрабатывает команду FAVORITE
    :param callback: CallbackQuery
    :param state: FSMContext
    :param session: сессия для работы с базой
    :return: None
    """
    await handle_favorite(
        session=session, callback=callback, cache=state, user_id=callback.from_user.id
    )
