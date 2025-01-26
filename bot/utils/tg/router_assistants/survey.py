from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import CallbackQuery, Message
from cache.button_cache import fill_in_params_on_buttons
from cache.get_data import get_data_from_cache
from config.settings import settings
from keyboards.inline import InlineKbForSurvey
from utils.buttons import ParseDataFromCb
from utils.constants.api_data import RATING_SORT
from utils.constants.cache_keys import BUTTONS_CACHE, COMMAND_CACHE, PARAMS_CACHE
from utils.enums.commands import Commands
from utils.enums.items import SortItem
from utils.response_formats import get_text_for_survey


async def go_to_selection_items(
    message: Message,
    cache: FSMContext,
    data_fsm: State,
    command: Commands,
    text: str,
    sort_field: str = RATING_SORT,
    combine_selection: bool = True,
    change_cache: bool = True,
) -> None:
    """
    Переходит на стадию выбора новых элементов и дополняет данные в параметрах

    :param message: Message
    :param cache: кэш с данными
    :param data_fsm: State
    :param command: Commands
    :param text: текст для отправки
    :param sort_field: поле для сортировки
    :param combine_selection: True, если можно комбинировать элементы, иначе False
    :param change_cache: True, если нужно обновлять и добавлять данные в кэш, иначе False
    :return: None
    """
    markup, buttons = InlineKbForSurvey.get_kb_to_select_buttons(data_fsm)
    await cache.set_state(data_fsm)
    await cache.update_data({COMMAND_CACHE: command, BUTTONS_CACHE: buttons})
    if change_cache is False:
        await message.answer(
            text=get_text_for_survey(text, combine_selection),
            reply_markup=markup,
        )
        return
    data = {
        "page": 1,
        "limit": settings.API.NUMBER_FILMS,
        "sortField": sort_field,
        "sortType": [SortItem.DESCEND],
    }
    params: dict | None = await get_data_from_cache(PARAMS_CACHE, cache=cache)
    if params is None:
        await cache.update_data({PARAMS_CACHE: data})
    else:
        params.update(data)
    await message.answer(
        text=get_text_for_survey(text, combine_selection),
        reply_markup=markup,
    )


async def move_to_new_stage(
    callback: CallbackQuery,
    cache: FSMContext,
    data_fsm: State,
    text: str,
    combine_selection: bool = True,
) -> None:
    """
    Переходит на новый этап опроса без сохранения данных

    :param callback: CallbackQuery
    :param cache: кэш с данными
    :param data_fsm: State
    :param text: текст для отправки
    :param combine_selection: True, если можно комбинировать элементы, иначе False
    :return: None
    """
    markup, buttons = InlineKbForSurvey.get_kb_to_select_buttons(data_fsm)
    await cache.set_state(data_fsm)

    await cache.update_data({BUTTONS_CACHE: buttons})
    await callback.message.edit_text(
        text=get_text_for_survey(text, combine_selection),
        reply_markup=markup,
    )


async def save_info_to_cache(
    cache: FSMContext,
    key: str,
    parse_data: ParseDataFromCb,
) -> None:
    """
    Сохраняет информацию в кэш
    :param cache: кэш с данными
    :param key: ключ для сохранения
    :param parse_data: ParseDataFromCb
    :return: None
    """
    await fill_in_params_on_buttons(
        cache=cache,
        key=key,
        get_cb=parse_data,
    )


async def save_info_and_move_to_new_stage(
    callback: CallbackQuery,
    cache: FSMContext,
    key: str,
    parse_data: ParseDataFromCb,
    data_fsm: State,
    text: str,
    combine_selection: bool = True,
) -> None:
    """
    Сохраняет информацию в кэш и переходит на новый этап опроса
    :param callback: CallbackQuery
    :param cache: кэш с данными
    :param key: ключ для сохранения
    :param parse_data: ParseDataFromCb
    :param data_fsm: State
    :param text: текст для отправки
    :param combine_selection: True, если можно комбинировать элементы, иначе False
    :return: None
    """
    await save_info_to_cache(cache, key, parse_data)
    await move_to_new_stage(callback, cache, data_fsm, text, combine_selection)
