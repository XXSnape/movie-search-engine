import locale
from collections.abc import Iterable
from datetime import date, datetime
from logging import getLogger

from utils.constants.output_for_user import COMPLETE_SELECTION_OUTPUT
from utils.validators.validate_data import check_first_arg

logger = getLogger(name=__name__)


def standard_format_output(string: str | int) -> str:
    """
    Обрабатывает строку для вывода в телеграмме
    :param string: текст
    :return: обработанная строка
    """
    return f"<b><i><u>{string}</u></i></b>"


def build_text(string: str | int) -> str:
    """
    Выделяет текст жирным в телеграме
    :param string: текст
    :return: обработанная строка
    """
    return f"<b>{string}</b>"


def join_by_sep(data: Iterable[str], sep: str = ", ", start: str = "") -> str | None:
    """
    Соединяет данные по разделителю. Возвращает None, если нет данных
    :param data: объект из строк
    :param sep: разделитель
    :param start: начальное значение
    :return: соединенная строка или None
    """
    if not data:
        return None
    return start + sep.join(data)


def present_data(json: dict, bad_values: tuple = (0, "", None, "\n")) -> str:
    """
    Конвертирует словарь данных в текст для отображения в телеграме
    :param json: словарь с данными
    :param bad_values: значения, которые не нужно выводить пользователю
    :return: преобразованная строка
    """
    return "\n\n".join(
        f"{standard_format_output(key)}: {value}"
        for key, value in json.items()
        if value not in bad_values
    )


@check_first_arg
def get_amount_in_rubles(amount: int, currency: str) -> int | None:
    """
    Переводит валюту в рубли
    :param amount: количество денег
    :param currency: валюта
    :return: количество денег в рублях или None, если валюта неизвестна
    """
    transfer_to_rubles = {
        "$": 96,
        "₽": 1,
        "₹": 1.15,
        "€": 104,
        "₫": 0.003,
        "₪": 25,
        "₩": 0.07,
        "฿": 2.8,
        "¥": 0.6,
        "£": 125,
    }
    ratio = transfer_to_rubles.get(currency)
    if ratio is None:
        return None
    return int(amount * ratio)


@check_first_arg
def get_pretty_number(amount: int) -> str:
    """
    Преобразует большую сумму денег в читабельный вид
    :param amount: сумма денег
    :return: строка в формате DDD DDD
    """
    sum_in_rubles = str(amount)[::-1]
    return "".join(
        sum_in_rubles[ind : ind + 3] + " " for ind in range(0, len(sum_in_rubles), 3)
    )[::-1][1:]


def get_pretty_date(date_string: str) -> str | None:
    """
    Переводит дату на русский язык
    :param date_string: дата
    :return: строка или None, если дата в неверном формате
    """
    locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
    try:
        date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    except (ValueError, TypeError) as e:
        logger.exception(e)
        return None
    return date.strftime("%d %B %Y")


@check_first_arg
def get_pretty_length_movie(minutes: int) -> str:
    """
    Конвертирует минуты в часы
    :param minutes: количество минут
    :return: строка с количеством часов и минут
    """
    hours = minutes // 60
    minutes = minutes % 60
    if hours:
        return f"Часов:  {hours}   Минут:  {minutes}"
    return f"Минут: {minutes}."


def get_text_for_survey(data: str, combine_selection: bool) -> str:
    """
    Генерирует текст для пользователя при опросе
    :param data: данные
    :param combine_selection: True, если элементы могут быть совместимы, иначе False
    :return: текст для пользователя при опросе
    """
    start = f"Чтобы выбрать {data}, нажмите 1 раз на кнопку.\n\n"
    middle = "Для отмены выбора, нажмите {} раза.\n\n".format(
        "3" if combine_selection else "2"
    )
    end = f"В конце нажмите «{COMPLETE_SELECTION_OUTPUT}»"

    if combine_selection:
        return f"{start}Чтобы выбрать комбинацию, нажмите 2 раза.\n\n{middle}{end}"
    return f"{start}{middle}{end}"


def get_russian_date(cur_date: date, is_time_displayed: bool = True) -> str:
    """
    Переводит дату на русский язык
    :param cur_date: дата
    :param is_time_displayed: True, если нужно, чтобы отображалось время, иначе False
    :return: дата на русском языке
    """
    locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
    if is_time_displayed:
        return cur_date.strftime("%d %B %Y %H:%M:%S")
    return cur_date.strftime("%d %B %Y")
