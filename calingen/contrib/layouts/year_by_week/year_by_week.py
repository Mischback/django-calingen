# SPDX-License-Identifier: MIT

""":class:`~calingen.interfaces.plugin_api.LayoutProvider` implementation for a year's calender."""

# Python imports
import logging
from datetime import date, timedelta

# app imports
from calingen.interfaces.plugin_api import LayoutProvider

logger = logging.getLogger(__name__)


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

        # the first day of the calendar is the monday before [YEAR]-01-01
        first_yearday = date(target_year, 1, 1) - timedelta(
            days=date(target_year, 1, 1).weekday()
        )
        # the last day of the calendar is the sunday after [YEAR]-12-31
        last_yearday = date(target_year, 12, 31) + timedelta(
            days=(7 - date(target_year, 12, 31).weekday())
        )

        # initialize the invariant
        day = first_yearday
        while day < last_yearday:
            logger.debug(day)

            # increment the invariant
            day = day + timedelta(days=1)

        raise NotImplementedError("to be done")
