from aiogram.fsm.context import FSMContext
from utils.constants.cache_keys import PARAMS_CACHE

from .get_data import get_data_from_cache


async def fill_in_params_on_key(
    key: str, data: list[str] | str, cache: FSMContext
) -> dict:
    """
    Заполняет параметры запроса информацией
    :param key: ключ, по которому вставить данные
    :param data: данные для запроса
    :param cache: кэш с данными
    :return: обновленные параметры
    """
    params = await get_data_from_cache(PARAMS_CACHE, cache=cache)
    if data:
        params[key] = data
    return params
