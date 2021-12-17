# SPDX-License-Identifier: MIT

""":class:`~calingen.interfaces.plugin_api.LayoutProvider` implementation for a year's calender."""

# app imports
from calingen.interfaces.plugin_api import LayoutProvider


class YearByWeek(LayoutProvider):
    """A very simple implementation of a list of events."""

    name = "Year by Week"
    paper_size = "a5"
    orientation = "portrait"
    _template = "year_by_week/tex/year_by_week.tex"

    @classmethod
    def prepare_context(cls, context):  # noqa: D102
        raise NotImplementedError("to be done")
