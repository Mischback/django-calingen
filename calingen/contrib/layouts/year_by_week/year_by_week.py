# SPDX-License-Identifier: MIT

""":class:`~calingen.interfaces.plugin_api.LayoutProvider` implementation for a year's calender."""

# Python imports
import logging
from datetime import date, timedelta

# app imports
from calingen.interfaces.plugin_api import LayoutProvider

logger = logging.getLogger(__name__)


class CalendarDay:
    """Layout-specific class to manage calendar days."""

    def __init__(self, date):
        self.date = date


class CalendarWeek:
    """Layout-specific class to manage calendar weeks."""

    def __init__(self):
        self.calendarweek = None
        self.month_string = None
        self.days = []

        self.populate_week = self._populate_week
        self.check_turnover = self._check_turnover

    def add_day(self, day):
        """Add a layout-specific day object to this week."""
        self.populate_week(day.date)

        self.days.append(day)

        self.check_turnover(day.date)

    @property
    def is_empty(self):
        """Flag to indicate, if this object already contains days."""
        return not self.days

    def _check_turnover(self, date_of_day):
        reference = self.days[0].date

        # no turnover, just return
        if reference.month == date_of_day.month:
            return

        if reference.year != date_of_day.year:
            self.month_string = (
                "{month_ref} {year_ref}/{month_this} {year_this}".format(
                    month_ref=reference.strftime("%B"),
                    year_ref=reference.year,
                    month_this=date_of_day.strftime("%B"),
                    year_this=date_of_day.year,
                )
            )
        else:
            self.month_string = "{month_ref}/{month_this}".format(
                month_ref=reference.strftime("%B"),
                month_this=date_of_day.strftime("%B"),
            )
        # Turnovers may happen only once per week, so provide noop() method
        # after first usage.
        self.check_turnover = self._noop

    def _populate_week(self, date_of_day):
        # isocalendar() returns a tuple of (year, week, weekday)
        self.calendarweek = date_of_day.isocalendar()[1]

        # as this method is only executed once (per week), just apply the month
        # of the given day
        self.month_string = date_of_day.strftime("%B")

        # Population of the week object is a one-time operation, so provide the
        # noop() method after the first usage.
        self.populate_week = self._noop

    def _noop(self, *args, **kwargs):
        """Just a generic no op method."""
        pass

    def __repr__(self):  # noqa: D105
        return "<CalendarWeek [{}] {}>".format(self.calendarweek, self.days[0].date)

    def __str__(self):  # noqa: D105
        return "[{}]".format(self.calendarweek)


class YearByWeek(LayoutProvider):
    """A very simple implementation of a list of events."""

    name = "Year by Week"
    paper_size = "a5"
    orientation = "portrait"
    _template = "year_by_week/tex/year_by_week.tex"

    @classmethod
    def prepare_context(cls, context):  # noqa: D102
        # get the target year from context
        target_year = context.get("target_year")

        # The first day of the calendar is the monday before [YEAR]-01-01
        # date().weekday() = 0 for Mondays, 6 for Sundays
        first_yearday = date(target_year, 1, 1) - timedelta(
            days=date(target_year, 1, 1).weekday()
        )
        # The last day of the calendar is the sunday after [YEAR]-12-31
        # date().weekday() = 0 for Mondays, 6 for Sundays
        # Note: This may seem to be "off by one", but this enables the while-loop
        # to match against "<" instead of "<=".
        last_yearday = date(target_year, 12, 31) + timedelta(
            days=(7 - date(target_year, 12, 31).weekday())
        )

        # prepare result
        weeklist = []
        this_week = CalendarWeek()
        # initialize the invariant
        day = first_yearday
        while day < last_yearday:
            # logger.debug(day)

            if day.weekday() == 0:
                if not this_week.is_empty:
                    weeklist.append(this_week)
                    this_week = CalendarWeek()

            this_day = CalendarDay(day)
            this_week.add_day(this_day)

            # increment the invariant
            day = day + timedelta(days=1)
        # append the final week to the result list
        if not this_week.is_empty:
            weeklist.append(this_week)

        logger.debug(weeklist)

        raise NotImplementedError("to be done")
