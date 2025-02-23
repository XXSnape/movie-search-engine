from aiogram.fsm.context import FSMContext
from utils.buttons import ParseDataFromCb
from utils.constants.cache_keys import (
    BUTTONS_CACHE,
    BUTTONS_KB_CACHE,
    FAVORITE_INDEX_CACHE,
    KEYBOARD_CACHE,
    SIZES_CACHE,
)
from utils.constants.router_keys import ANY_PLATFORM_ROUTER
from utils.enums.items import TypeSelection

from .fill_in_cache import fill_in_params_on_key
from .get_data import get_data_from_cache


async def fill_in_params_on_buttons(
    cache: FSMContext, key: str, get_cb: ParseDataFromCb
) -> None:
    """
    Собирает данные запроса и грузит их в кэш
    :param cache: кэш с данными
    :param key: ключ, по которому хранятся данные в параметрах
    :param get_cb: ParseDataFromCb
    :return: None
    """
    data = await get_data_from_buttons(cache, get_cb)
    await fill_in_params_on_key(key=key, data=data, cache=cache)


async def get_data_from_buttons(
    cache: FSMContext, get_cb: ParseDataFromCb
) -> list[str]:
    """
    Обрабатывает данные из кнопок в кэше после опроса.
    Добавляет +, если элементы должны быть совместны

    :param cache: кэш с данными
    :param get_cb: ParseDataFromCb
    :return: список с параметрами для запроса
    """
    buttons = await get_data_from_cache(BUTTONS_CACHE, cache=cache)
    data = []
    for btn in buttons[:-2]:
        if btn[1] == ANY_PLATFORM_ROUTER:
            continue
        result, cb = get_cb(btn)
        if cb.num_clicks == TypeSelection.CLASSIC_CHOICE:
            data.append(result)
        elif cb.num_clicks == TypeSelection.COMBINED_CHOICE:
            data.append("+" + result)
    return data


async def get_buttons_kb_data(cache: FSMContext) -> tuple[list, int, list[int]]:
    """
    Получает данные о клавиатуре из кэша
    :param cache: кэш с данными
    :return: список кнопок, индекс фильма из избранного, размеры клавиатуры
    """
    data = await get_data_from_cache(KEYBOARD_CACHE, cache=cache)
    return data[BUTTONS_KB_CACHE], data[FAVORITE_INDEX_CACHE], data[SIZES_CACHE]
