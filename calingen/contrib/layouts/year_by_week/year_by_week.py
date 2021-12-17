# SPDX-License-Identifier: MIT

""":class:`~calingen.interfaces.plugin_api.LayoutProvider` implementation for a year's calender."""

# Python imports
import logging
from datetime import date, timedelta

# Django imports
from django.template.defaultfilters import date as _date

# app imports
from calingen.constants import EventCategory
from calingen.interfaces.plugin_api import LayoutProvider

logger = logging.getLogger(__name__)


class CalendarDay:
    """Layout-specific class to manage calendar days."""

    def __init__(self, date, date_entries):
        self.date = date

        # filter date_entries into categories
        self.holidays = [
            x.title for x in date_entries if x.category == EventCategory.HOLIDAY
        ]
        self.annuals = [
            x.title
            for x in date_entries
            if x.category == EventCategory.ANNUAL_ANNIVERSARY
        ]


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
                    month_ref=_date(reference, "F"),
                    year_ref=reference.year,
                    month_this=_date(date_of_day, "F"),
                    year_this=date_of_day.year,
                )
            )
        else:
            self.month_string = "{month_ref}/{month_this}".format(
                month_ref=_date(reference, "F"),
                month_this=_date(date_of_day, "F"),
            )

        # Turnovers may happen only once per week, so provide noop() method
        # after first usage.
        self.check_turnover = self._noop

        logger.debug(self.month_string)

    def _populate_week(self, date_of_day):
        # isocalendar() returns a tuple of (year, week, weekday)
        self.calendarweek = date_of_day.isocalendar()[1]

        # as this method is only executed once (per week), just apply the month
        # of the given day
        self.month_string = _date(date_of_day, "F")

        # Population of the week object is a one-time operation, so provide the
        # noop() method after the first usage.
        self.populate_week = self._noop

    def _noop(self, *args, **kwargs):
        """Just a generic no op method."""
        pass

    def __repr__(self):  # noqa: D105
        return "<CalendarWeek [{}] {}>".format(
            self.calendarweek, self.days[0].date
        )  # pragma: nocover

    def __str__(self):  # noqa: D105
        return "[{}]".format(self.calendarweek)  # pragma: nocover


class YearByWeek(LayoutProvider):
    """A very simple implementation of a list of events."""

    name = "Year by Week"
    paper_size = "a5"
    orientation = "portrait"
    _template = "year_by_week/tex/year_by_week.tex"

    @classmethod
    def prepare_context(cls, context):  # noqa: D102
        # values from the context for processing
        target_year = context.get("target_year")
        entries = context.get("entries", [])

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
            if day.weekday() == 0:
                if not this_week.is_empty:
                    weeklist.append(this_week)
                    this_week = CalendarWeek()

            # This may look rather complex but is nothing more than filtering
            # the "entries" by day and feeding a list of entries into the
            # constructor of the CalendarDay class.
            this_day = CalendarDay(
                day,
                [
                    x
                    for x in entries
                    if x.timestamp.date().day == day.day
                    and x.timestamp.date().month == day.month
                ],
            )
            this_week.add_day(this_day)

            # increment the invariant
            day = day + timedelta(days=1)
        # append the final week to the result list
        if not this_week.is_empty:
            weeklist.append(this_week)

        context["weeklist"] = weeklist

        return context
