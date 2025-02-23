import calendar
from datetime import datetime

from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback
from aiogram_calendar.schemas import SimpleCalAct, highlight, superscript
from keyboards.inline.keyboards.command_kb import InlineKbForCommand
from utils.constants.output_for_user import DATE_EXISTS_OUTPUT, REQUIRE_ACTION_OUTPUT


class ExtendedSimpleCalendar(SimpleCalendar):
    """
    Расширенный SimpleCalendar
    """

    def __init__(
        self,
        locale: str = None,
        cancel_btn: str = None,
        today_btn: str = None,
        show_alerts: bool = False,
        available_dates: list[datetime] | None = None,
    ):
        """
        Инициализация календаря
        :param available_dates: список доступных дат или None
        """
        super().__init__(locale, cancel_btn, today_btn, show_alerts)
        self.available_dates = available_dates

    async def start_calendar(
        self,
        year: int = datetime.now().year,
        month: int = datetime.now().month,
    ) -> InlineKeyboardMarkup:
        """
        Creates an inline keyboard with the provided year and month
        :param int year: Year to use in the calendar, if None the current year is used.
        :param int month: Month to use in the calendar, if None the current month is used.
        :return: Returns InlineKeyboardMarkup object with the calendar.
        """

        today = datetime.now()
        now_weekday = self._labels.days_of_week[today.weekday()]
        now_month, now_year, now_day = today.month, today.year, today.day

        def highlight_month():
            month_str = self._labels.months[month - 1]
            if now_month == month and now_year == year:
                return highlight(month_str)
            return month_str

        def highlight_weekday():
            if now_month == month and now_year == year and now_weekday == weekday:
                return highlight(weekday)
            return weekday

        def format_day_string():
            date_to_check = datetime(year, month, day)
            if date_to_check in self.available_dates:
                return str(day) + DATE_EXISTS_OUTPUT
            if self.min_date and date_to_check < self.min_date:
                return superscript(str(day))
            elif self.max_date and date_to_check > self.max_date:
                return superscript(str(day))
            return str(day)

        def highlight_day():
            day_string = format_day_string()
            # if now_month == month and now_year == year and now_day == day:
            #     return highlight(day_string)
            return day_string

        # building a calendar keyboard
        kb = []

        # inline_kb = InlineKeyboardMarkup(row_width=7)
        # First row - Year
        years_row = []
        years_row.append(
            InlineKeyboardButton(
                text="<<",
                callback_data=SimpleCalendarCallback(
                    act=SimpleCalAct.prev_y, year=year, month=month, day=1
                ).pack(),
            )
        )
        years_row.append(
            InlineKeyboardButton(
                text=str(year) if year != now_year else highlight(year),
                callback_data=self.ignore_callback,
            )
        )
        years_row.append(
            InlineKeyboardButton(
                text=">>",
                callback_data=SimpleCalendarCallback(
                    act=SimpleCalAct.next_y, year=year, month=month, day=1
                ).pack(),
            )
        )
        kb.append(years_row)

        # Month nav Buttons
        month_row = []
        month_row.append(
            InlineKeyboardButton(
                text="<",
                callback_data=SimpleCalendarCallback(
                    act=SimpleCalAct.prev_m, year=year, month=month, day=1
                ).pack(),
            )
        )
        month_row.append(
            InlineKeyboardButton(
                text=highlight_month(), callback_data=self.ignore_callback
            )
        )
        month_row.append(
            InlineKeyboardButton(
                text=">",
                callback_data=SimpleCalendarCallback(
                    act=SimpleCalAct.next_m, year=year, month=month, day=1
                ).pack(),
            )
        )
        kb.append(month_row)

        # Week Days
        week_days_labels_row = []
        for weekday in self._labels.days_of_week:
            week_days_labels_row.append(
                InlineKeyboardButton(
                    text=highlight_weekday(), callback_data=self.ignore_callback
                )
            )
        kb.append(week_days_labels_row)

        # Calendar rows - Days of month
        month_calendar = calendar.monthcalendar(year, month)

        for week in month_calendar:
            days_row = []
            for day in week:
                if day == 0:
                    days_row.append(
                        InlineKeyboardButton(
                            text=" ", callback_data=self.ignore_callback
                        )
                    )
                    continue
                days_row.append(
                    InlineKeyboardButton(
                        text=highlight_day(),
                        callback_data=SimpleCalendarCallback(
                            act=SimpleCalAct.day, year=year, month=month, day=day
                        ).pack(),
                    )
                )
            kb.append(days_row)

        # nav today & cancel button
        cancel_row = []
        cancel_row.append(
            InlineKeyboardButton(
                text=self._labels.cancel_caption,
                callback_data=SimpleCalendarCallback(
                    act=SimpleCalAct.cancel, year=year, month=month, day=day
                ).pack(),
            )
        )
        cancel_row.append(
            InlineKeyboardButton(text=" ", callback_data=self.ignore_callback)
        )
        cancel_row.append(
            InlineKeyboardButton(
                text=self._labels.today_caption,
                callback_data=SimpleCalendarCallback(
                    act=SimpleCalAct.today, year=year, month=month, day=day
                ).pack(),
            )
        )
        kb.append(cancel_row)
        return InlineKeyboardMarkup(row_width=7, inline_keyboard=kb)

    async def process_day_select(self, data, query):
        """Если выбранной даты нет в списке доступных, возвращается False, None"""
        date = datetime(int(data.year), int(data.month), int(data.day))
        if self.available_dates and date not in self.available_dates:
            await query.answer(
                f"Выбирайте дату с {DATE_EXISTS_OUTPUT}",
                show_alert=self.show_alerts,
            )
            return False, None
        return await super().process_day_select(data, query)

    async def process_selection(
        self, query: CallbackQuery, data: SimpleCalendarCallback
    ) -> tuple:
        """
        Process the callback_query. This method generates a new calendar if forward or
        backward is pressed. This method should be called inside a CallbackQueryHandler.
        :param query: callback_query, as provided by the CallbackQueryHandler
        :param data: callback_data, dictionary, set by calendar_callback
        :return: Returns a tuple (Boolean,datetime), indicating if a date is selected
                    and returning the date if so.
        """
        if data.act == SimpleCalAct.cancel:
            await query.message.edit_text(
                text=REQUIRE_ACTION_OUTPUT,
                reply_markup=InlineKbForCommand.get_kb_to_select_command(),
            )
            return False, None
        return await super().process_selection(query, data)
