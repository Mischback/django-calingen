# SPDX-License-Identifier: MIT

""":class:`~calingen.interfaces.plugin_api.LayoutProvider` implementation for a year's calendar.

Warnings
--------
This layout is included in **django-calingen**'s CI test setup, mainly to verify
that the :func:`TeX escaping <calingen.templatetags.calingen_escape.escape_tex>`
is working.

This may be object to future changes.
"""

# Python imports
from datetime import date, timedelta

# Django imports
from django.template.defaultfilters import date as _date

# app imports
from calingen.constants import EventCategory
from calingen.interfaces.plugin_api import LayoutProvider


class CalendarDay:
    """Layout-specific class to manage calendar days.

    Parameters
    ----------
    date : datetime.date
        The Python representation of the date.
    date_entries : list
        A list of ``entries`` for the given ``date`` (will be a subset of the
        provided :class:`calingen.interfaces.data_exchange.CalendarEntryList`
        and each entry is expected to be an instance of
        :class:`calingen.interfaces.data_exchange.CalendarEntry`).
    """

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
        """Add a layout-specific day object to this week.

        This method is the actual public entry point of this class, allowing
        ``day`` objects to be added to the instance.

        Parameters
        ----------
        day : calingen.contrib.layouts.year_by_week.year_by_week.CalendarDay
            A layout-specific representation of a single ``day``, including its
            actual ``date`` (:py:obj:`datetime.date`) and instances of
            :class:`calingen.interfaces.data_exchange.CalendarEntry` associated
            with that ``date``.
        """
        self.populate_week(day.date)

        self.days.append(day)

        self.check_turnover(day.date)

    @property
    def is_empty(self):
        """Flag to indicate, if this object already contains days."""
        return not self.days

    def _check_turnover(self, date_of_day):
        """Update the ``month_string``.

        While adding days to this object, a *turnover* may happen, meaning that
        during that week a new month starts.

        This method updates the ``month_string`` attribute accordingly.

        As there can only be one *turnover* during any given week,
        :attr:`~calingen.contrib.layouts.year_by_week.year_by_week.YearByWeek.check_turnover`
        is substituted with
        :meth:`~calingen.contrib.layouts.year_by_week.year_by_week.YearByWeek._noop`
        during its execution.

        Warnings
        --------
        This is a private method, other methods should use
        :attr:`~calingen.contrib.layouts.year_by_week.year_by_week.YearByWeek.check_turnover`
        to ensure performance.

        Parameters
        ----------
        date_of_day : datetime.date
            A Python date representation.
        """
        reference = self.days[0].date

        # no turnover, just return
        if reference.month == date_of_day.month:
            return

        if reference.year != date_of_day.year:
            # Translation of month names
            # https://stackoverflow.com/a/6991918
            self.month_string = (
                "{month_ref} {year_ref}/{month_this} {year_this}".format(
                    month_ref=_date(reference, "F"),
                    year_ref=reference.year,
                    month_this=_date(date_of_day, "F"),
                    year_this=date_of_day.year,
                )
            )
        else:
            # Translation of month names
            # https://stackoverflow.com/a/6991918
            self.month_string = "{month_ref}/{month_this}".format(
                month_ref=_date(reference, "F"),
                month_this=_date(date_of_day, "F"),
            )

        # Turnovers may happen only once per week, so provide noop() method
        # after first usage.
        self.check_turnover = self._noop

    def _populate_week(self, date_of_day):
        """Set the object's meta data, e.g. number of the calendar week.

        This is a one-time operation that is performed on the first call to
        :meth:`~calingen.contrib.layouts.year_by_week.year_by_week.YearByWeek.add_day`.
        During that call,
        :attr:`~calingen.contrib.layouts.year_by_week.year_by_week.YearByWeek.populate_week`
        is substituted with
        :meth:`~calingen.contrib.layouts.year_by_week.year_by_week.YearByWeek._noop`.

        Warnings
        --------
        This is a private method, other methods should use
        :attr:`~calingen.contrib.layouts.year_by_week.year_by_week.YearByWeek.populate_week`
        to ensure performance.

        Parameters
        ----------
        date_of_day : datetime.date
            A Python date representation.
        """
        # isocalendar() returns a tuple of (year, week, weekday)
        self.calendarweek = date_of_day.isocalendar()[1]

        # as this method is only executed once (per week), just apply the month
        # of the given day
        # Translation of month names
        # https://stackoverflow.com/a/6991918
        self.month_string = _date(date_of_day, "F")

        # Population of the week object is a one-time operation, so provide the
        # noop() method after the first usage.
        self.populate_week = self._noop

    def _noop(self, *args, **kwargs):
        """Just a generic no op method.

        This method is used to substitute
        :attr:`~calingen.contrib.layouts.year_by_week.year_by_week.YearByWeek.populate_week`
        and
        :attr:`~calingen.contrib.layouts.year_by_week.year_by_week.YearByWeek.check_turnover`
        during processing.
        """
        pass

    def __repr__(self):  # noqa: D105
        return "<CalendarWeek [{}] {}>".format(
            self.calendarweek, self.days[0].date
        )  # pragma: nocover

    def __str__(self):  # noqa: D105
        return "[{}]".format(self.calendarweek)  # pragma: nocover


class YearByWeek(LayoutProvider):
    """The actual implementation of the layout.

    :meth:`~calingen.contrib.layouts.year_by_week.year_by_week.YearByWeek.prepare_context`
    is used to create a year's full representation, grouping the days by week
    and matching the ``entries`` to the given day.

    Warnings
    --------
    The provided templates create a document targeted at German users. You may
    override the templates to (fully) support other languages.

    Notes
    -----
    To customize the generated TeX-sources, the following templates may be
    overridden:

    - ``year_by_week/tex/base.tex``: Speaking in TeX-terms: the preamble of
      the document, including package definitions.
    - ``year_by_week/tex/year_by_week.tex``: Speaking in TeX-terms:
      the document's body.
    """

    name = "Year by Week"
    paper_size = "a5"
    orientation = "portrait"
    layout_type = "tex"
    _template = "year_by_week/tex/year_by_week.tex"

    @classmethod
    def prepare_context(cls, context):
        """Create a full year's representation and return it as ``weeklist``."""
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
