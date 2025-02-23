from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from config.settings import settings
from keyboards.inline.callback_factory.request_factory import RequestCbData
from keyboards.inline.keyboards.command_kb import InlineKbForCommand
from services.request import save_new_request, update_request
from sqlalchemy.ext.asyncio import AsyncSession
from utils.constants.cache_keys import (
    COMMAND_CACHE,
    MIN_PAGE_CACHE,
    PARAMS_CACHE,
    REQUEST_ID_CACHE,
)
from utils.constants.output_for_user import REQUIRE_ACTION_OUTPUT
from utils.enums.commands import Commands
from utils.enums.request_data import SelectActionWithRequest

router = Router(name=__name__)


@router.callback_query(
    RequestCbData.filter(F.options == SelectActionWithRequest.COMPLETE)
)
async def handle_end_of_dialog(
    callback: CallbackQuery,
    callback_data: RequestCbData,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    """
    Обрабатывает сохранение запроса.

    Все просмотренные пользователем фильмы в рамках конкретного запроса остаются в кэше.
    0 индекс - фильм, который просмотрен на наименьшей просмотренной странице.
    -1 индекс - на наибольшей.

    Так как на каждой странице по NUMBER_FILMS фильмов, если она не последняя,
    то последняя страница, на которой остановился пользователь высчитывается, как

    наименьшая страница, до которой доходил пользователь (сохранена в кэше) + (текущий индекс фильма в кэше // NUMBER_FILMS)

    :param callback: CallbackQuery
    :param callback_data: RequestCbData
    :param state: FSMContext
    :param session: сессия для работы с базой
    :return: None
    """
    data = await state.get_data()
    command = data.get(COMMAND_CACHE)
    if command not in (
        Commands.MOVIE_SEARCH,
        Commands.FAVORITE,
    ):
        min_page = data[MIN_PAGE_CACHE]
        cur_page = min_page + callback_data.index // settings.API.NUMBER_FILMS
        remain = callback_data.index % settings.API.NUMBER_FILMS
        params = data[PARAMS_CACHE]
        if data.get(REQUEST_ID_CACHE) is not None:
            await update_request(
                session=session,
                id=data.get(REQUEST_ID_CACHE),
                page=cur_page,
                index=remain,
            )
        else:
            await save_new_request(
                session=session,
                user_id=callback.from_user.id,
                params=params,
                page=cur_page,
                index=remain,
                command=command,
            )
    await callback.message.delete()
    await callback.message.answer(
        text=REQUIRE_ACTION_OUTPUT,
        reply_markup=InlineKbForCommand.get_kb_to_select_command(),
    )
