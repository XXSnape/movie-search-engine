from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from api import MovieAdvancedSearch
from cache.get_data import get_data_from_cache, get_request_and_len
from keyboards.inline.callback_factory.request_factory import RequestCbData
from keyboards.inline.keyboards.command_kb import InlineKbForCommand
from keyboards.inline.keyboards.request_kb import InlineKbForRequest
from services.request import delete_request, resume_request
from sqlalchemy.ext.asyncio import AsyncSession
from utils.constants.cache_keys import (
    COMMAND_CACHE,
    MIN_PAGE_CACHE,
    PARAMS_CACHE,
    REQUEST_ID_CACHE,
    REQUESTS_CACHE,
)
from utils.constants.output_for_user import (
    REQUEST_DELETED_OUTPUT,
    REQUIRE_ACTION_OUTPUT,
)
from utils.enums.request_data import SelectActionWithRequest
from utils.tg.switch_movie import send_first_movie

router = Router(name=__name__)


@router.callback_query(
    RequestCbData.filter(F.options == SelectActionWithRequest.RESUME)
)
async def handle_renewal_request(
    callback: CallbackQuery,
    callback_data: RequestCbData,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    """
    Делает запрос для актуализации данных

    :param callback: CallbackQuery
    :param callback_data: RequestCbData
    :param state: FSMContext
    :param session: сессия для работы с базой
    :return: None
    """
    request, _ = await get_request_and_len(idx=callback_data.index, cache=state)
    params = request.params
    new_request_id = await resume_request(session, request)
    params["page"] = 1
    await state.update_data(
        {
            COMMAND_CACHE: request.command,
            PARAMS_CACHE: params,
            MIN_PAGE_CACHE: 1,
            REQUEST_ID_CACHE: new_request_id,
        }
    )
    await send_first_movie(
        session=session,
        func=MovieAdvancedSearch.get_movies_and_len_by_advanced_params,
        tg_obj=callback,
        cache=state,
        params=request.params,
    )


@router.callback_query(
    RequestCbData.filter(F.options == SelectActionWithRequest.DELETE)
)
async def handle_request_deletion(
    callback: CallbackQuery,
    callback_data: RequestCbData,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    """
    Обрабатывает удаление запроса

    :param callback: CallbackQuery
    :param callback_data: RequestCbData
    :param state: FSMContext
    :param session: сессия для работы с базой
    :return: None
    """
    requests = await get_data_from_cache(REQUESTS_CACHE, cache=state)
    last_request = requests.pop(callback_data.index)
    await delete_request(session=session, id=last_request.id)
    length = len(requests)
    if length == 0:
        await callback.answer(
            f"{REQUEST_DELETED_OUTPUT}\nЗапросов больше нет",
            show_alert=True,
        )
        await callback.message.edit_text(
            text=REQUIRE_ACTION_OUTPUT,
            reply_markup=InlineKbForCommand.get_kb_to_select_command(),
        )
        return
    await callback.answer(f"{REQUEST_DELETED_OUTPUT}", show_alert=True)
    if len(requests) == callback_data.index:
        new_index = callback_data.index - 1
    else:
        new_index = callback_data.index
    request = requests[new_index]
    markup = InlineKbForRequest.get_kb_to_select_actions(idx=new_index, length=length)
    await callback.message.edit_text(text=request.text, reply_markup=markup)


@router.callback_query(RequestCbData.filter(F.options == SelectActionWithRequest.SEND))
async def handle_request_submission(
    callback: CallbackQuery,
    callback_data: RequestCbData,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    """
    Обрабатывает возобновление запроса

    :param callback: CallbackQuery
    :param callback_data: RequestCbData
    :param state: FSMContext
    :param session: сессия для работы с базой
    :return: None
    """
    request, _ = await get_request_and_len(idx=callback_data.index, cache=state)
    params = request.params
    params["page"] = request.page
    await state.update_data(
        {
            COMMAND_CACHE: request.command,
            PARAMS_CACHE: params,
            MIN_PAGE_CACHE: request.page,
            REQUEST_ID_CACHE: request.id,
        }
    )
    await send_first_movie(
        session=session,
        func=MovieAdvancedSearch.get_movies_and_len_by_advanced_params,
        tg_obj=callback,
        cache=state,
        idx=request.index,
        params=params,
        movie_index=request.index,
    )
