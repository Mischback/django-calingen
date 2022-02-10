# SPDX-License-Identifier: MIT

"""The actual implementations of :class:`~calingen.interfaces.plugin_api.EventProvider`.

The classes just collect the pre-defined holidays in their ``entries``
class attribute.

The pre-defined holidays use :py:obj:`dateutil.rrule.rrule` to define their
recurrence. Most of Germany's holidays are based off the Easter date, so
``rrule`` allows for easy definitions.
"""

# Python imports
from datetime import datetime

# Django imports
from django.utils.translation import gettext_lazy as _

# external imports
from dateutil.rrule import WE, YEARLY, rrule

# app imports
from calingen.constants import EventCategory
from calingen.interfaces.plugin_api import EventProvider

# The following constants simply provide all the available German Holidays
# These will be combined in the actual implementation classes, e.g. in
# GermanyFederal
NEUJAHR = (
    _("New Year"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 1, 1)),
)
"""New Year, January, 1st."""

HEILIGE_DREI_KOENIGE = (
    _("Epiphany"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 1, 6)),
)
"""Epiphany, January, 6th."""

FRAUENTAG = (
    _("Women's Day"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 3, 8)),
)
"""Women's Day, March, 8th."""

KARFREITAG = (
    _("Good Friday"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 1, 1), byeaster=-2),
)
"""Good Friday, the Friday before Easter.

Notes
-----
This holiday is based off the Easter date, which shifts from year to year.
"""

OSTER_SONNTAG = (
    _("Easter Sunday"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 1, 1), byeaster=0),
)
"""Easter Sunday.

Notes
-----
This holiday is based off the Easter date, which shifts from year to year.
"""

OSTER_MONTAG = (
    _("Easter Monday"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 1, 1), byeaster=1),
)
"""Easter Monday, the Monday after Easter.

Notes
-----
This holiday is based off the Easter date, which shifts from year to year.
"""

TAG_DER_ARBEIT = (
    _("Worker's Day"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 5, 1)),
)
"""Worker's Day, May, 1st."""

CHRISTI_HIMMELFAHRT = (
    _("Ascension"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 1, 1), byeaster=39),
)
"""Ascension, the Thursday 39 days after Easter.

Notes
-----
This holiday is based off the Easter date, which shifts from year to year.
"""

PFINGST_SONNTAG = (
    _("Pentecost Sunday"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 1, 1), byeaster=49),
)
"""Pentecost Sunday, the Sunday 49 days after Easter.

Notes
-----
This holiday is based off the Easter date, which shifts from year to year.
"""

PFINGST_MONTAG = (
    _("Pentecost Monday"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 1, 1), byeaster=50),
)
"""Pentecost Monday, the Monday 50 days after Easter.

Notes
-----
This holiday is based off the Easter date, which shifts from year to year.
"""

FRONLEICHNAM = (
    _("Corpus Christi"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 1, 1), byeaster=60),
)
"""Corpus Christi, the Thursday 60 days after Easter.

Notes
-----
This holiday is based off the Easter date, which shifts from year to year.
"""

MARIA_HIMMELFAHRT = (
    _("Assumption of Mary"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 8, 15)),
)
"""Assumption of Mary, August, 15th."""

WELTKINDERTAG = (
    _("Children's Day"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 9, 20)),
)
"""Children's Day, September, 20th."""

TAG_DER_DEUTSCHEN_EINHEIT = (
    _("Day of German Unity"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 10, 3)),
)
"""Day of German Unity, October, 3rd."""

REFORMATIONSTAG = (
    _("Reformation Day"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 10, 31)),
)
"""Reformation Day, October, 31st."""

ALLERHEILIGEN = (
    _("All Hallows"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 11, 1)),
)
"""All Hallows, November, 1st."""

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
"""Day of Repetance, the last Wednesday of November."""

ERSTER_WEIHNACHTSTAG = (
    _("Christmas Day"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 12, 25)),
)
"""Christmas Day, December, 25th."""

ZWEITER_WEIHNACHTSTAG = (
    _("Boxing Day"),
    EventCategory.HOLIDAY,
    rrule(freq=YEARLY, dtstart=datetime(1990, 12, 26)),
)
"""Boxing Day, December, 26th."""

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

    entries = FEDERAL_HOLIDAYS


class BadenWuerttemberg(GermanyFederal):
    """Provides holidays of Baden-Wuerttemberg."""

    title = _("Holidays of Baden-Württemberg")

    entries = FEDERAL_HOLIDAYS + [HEILIGE_DREI_KOENIGE, FRONLEICHNAM, ALLERHEILIGEN]


class Bayern(GermanyFederal):
    """Provides holidays of Bayern."""

    title = _("Holidays of Bayern")

    entries = FEDERAL_HOLIDAYS + [
        HEILIGE_DREI_KOENIGE,
        FRONLEICHNAM,
        MARIA_HIMMELFAHRT,
        ALLERHEILIGEN,
    ]


class Berlin(GermanyFederal):
    """Provides holidays of Berlin."""

    title = _("Holidays of Berlin")

    entries = FEDERAL_HOLIDAYS + [FRAUENTAG]


class Brandenburg(GermanyFederal):
    """Provides holidays of Brandenburg."""

    title = _("Holidays of Brandenburg")

    entries = FEDERAL_HOLIDAYS + [REFORMATIONSTAG]


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

    entries = FEDERAL_HOLIDAYS + [FRONLEICHNAM]


class NordrheinWestphalen(GermanyFederal):
    """Provides holidays of Nordrhein-Westphalen."""

    title = _("Holidays of Nordrhein-Westphalen")

    entries = FEDERAL_HOLIDAYS + [FRONLEICHNAM, ALLERHEILIGEN]


class RheinlandPfalz(NordrheinWestphalen):
    """Provides holidays of Rheinland-Pfalz."""

    title = _("Holidays of Rheinland-Pfalz")


class Saarland(GermanyFederal):
    """Provides holidays of Saarland."""

    title = _("Holidays of Saarland")

    entries = FEDERAL_HOLIDAYS + [FRONLEICHNAM, ALLERHEILIGEN, MARIA_HIMMELFAHRT]


class Sachsen(GermanyFederal):
    """Provides holidays of Sachsen."""

    title = _("Holidays of Sachsen")

    entries = FEDERAL_HOLIDAYS + [FRONLEICHNAM, BUSS_UND_BETTAG]


class SachsenAnhalt(GermanyFederal):
    """Provides holidays of Sachsen-Anhalt."""

    title = _("Holidays of Sachsen-Anhalt")

    entries = FEDERAL_HOLIDAYS + [HEILIGE_DREI_KOENIGE, REFORMATIONSTAG]


class Thueringen(GermanyFederal):
    """Provides holidays of Thueringen."""

    title = _("Holidays of Thüringen")

    entries = FEDERAL_HOLIDAYS + [FRONLEICHNAM, WELTKINDERTAG, REFORMATIONSTAG]
