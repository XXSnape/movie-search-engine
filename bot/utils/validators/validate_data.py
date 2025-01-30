from functools import wraps
from logging import getLogger
from typing import Any, Callable

logger = getLogger(name=__name__)


def check_first_arg[T, **P](func: Callable[P, T]) -> Callable[P, T]:
    """
    Декоратор, проверяющий первый аргумент, переданный в функцию
    :param func: Callable[P, T]
    :return: Callable[P, T]
    """

    @wraps(func)
    def wrapper(arg: P.args, *args: P.args) -> T:
        """
        Если первый аргумент не является числом, он и возвращается
        :param arg: аргумент для функции
        :return: результат переданной функции или переданный аргумент
        """
        if isinstance(arg, int) is False:
            return arg
        return func(arg, *args)

    return wrapper


def get_value(
    *keys,
    json: dict,
    format_result: str = None,
    bad_values: tuple = (None, 0, ""),
    return_result=None,
) -> Any:
    """
    Пытается получить значения по переданным ключам

    :param keys: ключи
    :param json: данные для обработки
    :param format_result: формат возвращаемого результата
    :param bad_values: значения, которые не должен видеть пользователь
    :param return_result: результат для возврата, если произойдет ошибка
    :return: Any
    """
    obj = json
    try:
        for key in keys:
            obj = obj[key]
        if obj in bad_values:
            return return_result
        if format_result:
            return format_result.format(obj)
        return obj
    except (KeyError, IndexError, TypeError):
        logger.info("Не найдены ключи %s", keys)
        return return_result


def get_value_by_different_keys(*keys, json: dict) -> Any:
    """
    Пытается получить значение по хотя бы одному из переданных ключей
    :param keys: ключи
    :param json: данные для обработки
    :return: Any
    """
    for key in keys:
        obj = json.get(key)
        if obj is not None:
            return obj
