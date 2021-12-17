# SPDX-License-Identifier: MIT

"""A simple list of all events."""

# local imports
from .year_by_week import YearByWeek  # noqa: F401

default_app_config = (
    "calingen.contrib.layouts.year_by_week.apps.CalingenLayoutYearByWeekConfig"
)
"""The path to the app's default configuration class.

Consider this *legacy code*. See
:djangoapi:`Django's documentation<applications/#configuring-applications>` for
details.

Notes
-----
While the layout is provided as a "standalone Django app", it is in fact nothing
more than an implementation of
:class:`~calingen.interfaces.plugin_api.LayoutProvider`. The actual magic of
registering the layout with the main app is not done in this app's
:class:`~django.apps.AppConfig`, but in this very file by importing the
:class:`~calingen.contrib.layouts.year_by_week.year_by_week.YearByWeek`
class.
"""
