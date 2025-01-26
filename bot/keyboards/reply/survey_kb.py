from datetime import datetime

from aiogram.types import ReplyKeyboardMarkup
from keyboards.reply.mixins.generate_kb import GenerateReplyKeyboardMixin
from utils.constants.router_keys import ANY_YEAR_ROUTER


class ReplyKbForSurvey(GenerateReplyKeyboardMixin):

    @classmethod
    def get_kb_for_select_years(cls) -> ReplyKeyboardMarkup:
        """
        Возвращает клавиатуру для выбора годов
        :return: ReplyKeyboardMarkup
        """
        year = str(datetime.utcnow().year)
        return cls._generate_reply_kb(
            ANY_YEAR_ROUTER,
            year,
            f"2020 {year}",
            "2017 2020",
            "2014 2017",
            "2010 2014",
            "2000 2010",
            "1990 2000",
            "1950 1990",
            input_field_placeholder="Годы:",
            sizes=(1, 1, 4),
        )
