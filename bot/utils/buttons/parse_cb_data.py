from collections.abc import Callable

from keyboards.inline.callback_factory.survey_factory import MovieCbData


class ParseDataFromCb:
    """
    Обрабатывает данные от пользователя
    """

    def __init__(self, storage: tuple[str], func: Callable = None) -> None:
        """
        Инициализирует объект
        :param storage: все доступные элементы
        :param func: функция для конвертации данных для api
        """
        self.storage = storage
        self.func = func

    def __call__(self, button: list[str, str]) -> tuple[str, MovieCbData]:
        """
        Вызывается для обработки информации о нажатой кнопки
        :param button: список из текста кнопки и ее данных
        :return:  результат для api и MovieCbData
        """
        _, cb = button
        cb = MovieCbData.unpack(cb)
        result = self.storage[cb.data]
        if self.func:
            result = self.func(result)
        return result, cb
