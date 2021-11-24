# SPDX-License-Identifier: MIT

""":class:`~calingen.interfaces.plugin_api.EventProvider` implementations for german holidays."""

# Python imports
from datetime import datetime

# external imports
from dateutil.rrule import YEARLY, rrule

# app imports
from calingen.interfaces.data_exchange import CalenderEntryList
from calingen.interfaces.plugin_api import EventProvider


class GermanyFederal(EventProvider):
    """Provides federal holidays of Germany."""

    title = "Holidays:Germany:Federal"

    holidays = [
        ("Neujahr", "HOLIDAY", rrule(freq=YEARLY, dtstart=datetime(1990, 1, 1))),
        ("Karfreitag", "HOLIDAY", rrule(freq=YEARLY, byeaster=-2)),
        ("Ostersonntag", "HOLIDAY", rrule(freq=YEARLY, byeaster=0)),
        ("Ostermontag", "HOLIDAY", rrule(freq=YEARLY, byeaster=1)),
        ("Pfingsten", "HOLIDAY", rrule(freq=YEARLY, byeaster=49)),
        ("Pfingstmontag", "HOLIDAY", rrule(freq=YEARLY, byeaster=50)),
        (
            "Tag der deutschen Einheit",
            "HOLIDAY",
            rrule(freq=YEARLY, dtstart=datetime(1990, 10, 3)),
        ),
        (
            "1. Weihnachtstag",
            "HOLIDAY",
            rrule(freq=YEARLY, dtstart=datetime(1990, 12, 25)),
        ),
        (
            "2. Weihnachtstag",
            "HOLIDAY",
            rrule(freq=YEARLY, dtstart=datetime(1990, 12, 26)),
        ),
    ]

    @classmethod
    def resolve(cls, year):  # noqa: D102

        result = CalenderEntryList()
        for i in cls.holidays:
            result.add_entry(
                None,
                title=i[0],
                category="HOLIDAY",
                start=i[2].between(
                    datetime(year, 1, 1), datetime(year, 12, 31), inc=True
                )[0],
            )
        return result


class TestProvider(GermanyFederal):  # noqa: D101

    title = "Holidays:TEST"
