# SPDX-License-Identifier: MIT

""":class:`~calingen.interfaces.plugin_api.EventProvider` implementations for german holidays."""

# Python imports
from datetime import datetime

# Django imports
from django.utils.translation import ugettext_lazy as _

# external imports
from dateutil.rrule import YEARLY, rrule

# app imports
from calingen.constants import EventType
from calingen.interfaces.data_exchange import CalenderEntryList
from calingen.interfaces.plugin_api import EventProvider

# The following constants simply provide all the available German Holidays
# These will be combined in the actual implementation classes, e.g. in
# GermanyFederal
NEUJAHR = (
    _("New Year"),
    EventType.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 1, 1)),
)
HEILIGE_DREI_KOENIGE = (
    _("Epiphany"),
    EventType.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 1, 6)),
)
# FRAUENTAG = (_("Women's Day"), EventType.HOLIDAY, rrule(freq=YEARLY, dtstart=datetime(1990, 3, 8)))
KARFREITAG = (_("Good Friday"), EventType.HOLIDAY, rrule(freq=YEARLY, byeaster=-2))
OSTER_SONNTAG = (_("Easter Sunday"), EventType.HOLIDAY, rrule(freq=YEARLY, byeaster=0))
OSTER_MONTAG = (_("Easter Monday"), EventType.HOLIDAY, rrule(freq=YEARLY, byeaster=1))
TAG_DER_ARBEIT = (
    _("Worker's Day"),
    EventType.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 5, 1)),
)
CHRISTI_HIMMELFAHRT = (
    _("Ascension"),
    EventType.HOLIDAY,
    rrule(freq=YEARLY, byeaster=39),
)
PFINGST_SONNTAG = (
    _("Penecost Sunday"),
    EventType.HOLIDAY,
    rrule(freq=YEARLY, byeaster=49),
)
PFINGST_MONTAG = (
    _("Pentecost Monday"),
    EventType.HOLIDAY,
    rrule(freq=YEARLY, byeaster=50),
)
FRONLEICHNAM = (_("Corpus Christi"), EventType.HOLIDAY, rrule(freq=YEARLY, byeaster=60))
TAG_DER_DEUTSCHEN_EINHEIT = (
    _("Day of German Unity"),
    EventType.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 10, 3)),
)
ALLERHEILIGEN = (
    _("All Hallows"),
    EventType.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 11, 1)),
)
ERSTER_WEIHNACHTSTAG = (
    _("Christmas Day"),
    EventType.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 12, 25)),
)
ZWEITER_WEIHNACHTSTAG = (
    _("Boxing Day"),
    EventType.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 12, 26)),
)

# The actual classes will use Germany's federal structure as a taxononmy.
# However, there are some holidays that are applicable to all states, these are
# aggregated in this list.
# Please note: OSTER_SONNTAG and PFINGS_SONNTAG are not really considered
# "holiday" in all states, but they are sundays nonetheless.
FEDERAL_HOLIDAYS = [
    NEUJAHR,
    KARFREITAG,
    OSTER_SONNTAG,
    OSTER_MONTAG,
    TAG_DER_ARBEIT,
    CHRISTI_HIMMELFAHRT,
    PFINGST_SONNTAG,
    PFINGST_MONTAG,
    TAG_DER_DEUTSCHEN_EINHEIT,
    ERSTER_WEIHNACHTSTAG,
    ZWEITER_WEIHNACHTSTAG,
]


class GermanyFederal(EventProvider):
    """Provides federal holidays of Germany."""

    title = _("German Federal Holidays")

    holidays = FEDERAL_HOLIDAYS

    @classmethod
    def resolve(cls, year):  # noqa: D102

        result = CalenderEntryList()
        for i in cls.holidays:
            result.add_entry(
                None,
                title=i[0],
                category=i[1],
                start=i[2].between(
                    datetime(year, 1, 1), datetime(year, 12, 31), inc=True
                )[0],
            )
        return result


class BadenWuerttemberg(GermanyFederal):
    """Provides holidays of Baden-Wuerttemberg."""

    title = _("Holidays of Baden-Württemberg")

    holidays = FEDERAL_HOLIDAYS + [HEILIGE_DREI_KOENIGE, FRONLEICHNAM, ALLERHEILIGEN]
