# SPDX-License-Identifier: MIT

""":class:`~calingen.interfaces.plugin_api.EventProvider` implementations for german holidays."""

# Python imports
from datetime import datetime

# Django imports
from django.utils.translation import ugettext_lazy as _

# external imports
from dateutil.rrule import WE, YEARLY, rrule

# app imports
from calingen.constants import EventCategory
from calingen.interfaces.data_exchange import CalenderEntryList
from calingen.interfaces.plugin_api import EventProvider

# The following constants simply provide all the available German Holidays
# These will be combined in the actual implementation classes, e.g. in
# GermanyFederal
NEUJAHR = (
    _("New Year"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 1, 1)),
)
HEILIGE_DREI_KOENIGE = (
    _("Epiphany"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 1, 6)),
)
FRAUENTAG = (
    _("Women's Day"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 3, 8)),
)
KARFREITAG = (
    _("Good Friday"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 1, 1), byeaster=-2),
)
OSTER_SONNTAG = (
    _("Easter Sunday"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 1, 1), byeaster=0),
)
OSTER_MONTAG = (
    _("Easter Monday"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 1, 1), byeaster=1),
)
TAG_DER_ARBEIT = (
    _("Worker's Day"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 5, 1)),
)
CHRISTI_HIMMELFAHRT = (
    _("Ascension"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 1, 1), byeaster=39),
)
PFINGST_SONNTAG = (
    _("Penecost Sunday"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 1, 1), byeaster=49),
)
PFINGST_MONTAG = (
    _("Pentecost Monday"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 1, 1), byeaster=50),
)
FRONLEICHNAM = (
    _("Corpus Christi"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 1, 1), byeaster=60),
)
MARIA_HIMMELFAHRT = (
    _("Assumption of Mary"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 8, 15)),
)
WELTKINDERTAG = (
    _("Children's Day"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 9, 20)),
)
TAG_DER_DEUTSCHEN_EINHEIT = (
    _("Day of German Unity"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 10, 3)),
)
REFORMATIONSTAG = (
    _("Reformation Day"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 10, 31)),
)
ALLERHEILIGEN = (
    _("All Hallows"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 11, 1)),
)
BUSS_UND_BETTAG = (
    _("Day of Repetance"),
    EventCategory.HOLIDAY,
    rrule(
        freq=YEARLY,
        dtstart=datetime(1990, 1, 1),
        bymonth=11,
        byweekday=WE,
        bymonthday=(16, 17, 18, 19, 20, 21, 22),
    ),
)
ERSTER_WEIHNACHTSTAG = (
    _("Christmas Day"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 12, 25)),
)
ZWEITER_WEIHNACHTSTAG = (
    _("Boxing Day"),
    EventCategory.HOLIDAY,
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


class Bayern(GermanyFederal):
    """Provides holidays of Bayern."""

    title = _("Holidays of Bayern")

    holidays = FEDERAL_HOLIDAYS + [
        HEILIGE_DREI_KOENIGE,
        FRONLEICHNAM,
        MARIA_HIMMELFAHRT,
        ALLERHEILIGEN,
    ]


class Berlin(GermanyFederal):
    """Provides holidays of Berlin."""

    title = _("Holidays of Berlin")

    holidays = FEDERAL_HOLIDAYS + [FRAUENTAG]


class Brandenburg(GermanyFederal):
    """Provides holidays of Brandenburg."""

    title = _("Holidays of Brandenburg")

    holidays = FEDERAL_HOLIDAYS + [REFORMATIONSTAG]


class Bremen(Brandenburg):
    """Provides holidays of Bremen."""

    title = _("Holidays of Bremen")


class Hamburg(Brandenburg):
    """Provides holidays of Hamburg."""

    title = _("Holidays of Hamburg")


class MecklenburgVorpommern(Brandenburg):
    """Provides holidays of Mecklenburg-Vorpommern."""

    title = _("Holidays of Mecklenburg-Vorpommern")


class Niedersachsen(Brandenburg):
    """Provides holidays of Niedersachsen."""

    title = _("Holidays of Niedersachsen")


class SchleswigHolstein(Brandenburg):
    """Provides holidays of Schleswig-Holstein."""

    title = _("Holidays of Schleswig-Holstein")


class Hessen(GermanyFederal):
    """Provides holidays of Hessen."""

    title = _("Holidays of Hessen")

    holidays = FEDERAL_HOLIDAYS + [FRONLEICHNAM]


class NordrheinWestphalen(GermanyFederal):
    """Provides holidays of Nordrhein-Westphalen."""

    title = _("Holidays of Nordrhein-Westphalen")

    holidays = FEDERAL_HOLIDAYS + [FRONLEICHNAM, ALLERHEILIGEN]


class RheinlandPfalz(NordrheinWestphalen):
    """Provides holidays of Rheinland-Pfalz."""

    title = _("Holidays of Rheinland-Pfalz")


class Saarland(GermanyFederal):
    """Provides holidays of Saarland."""

    title = _("Holidays of Saarland")

    holidays = FEDERAL_HOLIDAYS + [FRONLEICHNAM, ALLERHEILIGEN, MARIA_HIMMELFAHRT]


class Sachsen(GermanyFederal):
    """Provides holidays of Sachsen."""

    title = _("Holidays of Sachsen")

    holidays = FEDERAL_HOLIDAYS + [FRONLEICHNAM, BUSS_UND_BETTAG]


class SachsenAnhalt(GermanyFederal):
    """Provides holidays of Sachsen-Anhalt."""

    title = _("Holidays of Sachsen-Anhalt")

    holidays = FEDERAL_HOLIDAYS + [HEILIGE_DREI_KOENIGE, REFORMATIONSTAG]


class Thueringen(GermanyFederal):
    """Provides holidays of Thueringen."""

    title = _("Holidays of Thüringen")

    holidays = FEDERAL_HOLIDAYS + [FRONLEICHNAM, WELTKINDERTAG, REFORMATIONSTAG]
