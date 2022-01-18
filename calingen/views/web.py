# SPDX-License-Identifier: MIT

"""Provides the web views.

These views are not model-specific (see
:mod:`calingen.views.event` and :mod:`calingen.views.profile`) nor directly
related to render and compile layouts (see :mod:`calingen.views.generation`),
but provide representations of the app's data.

Please note: The focus of calingen is to create analogous, paper-based calendar
pages. These views are provided as convenience!
"""

# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

# app imports
from calingen.views.mixins import AllCalendarEntriesMixin, RestrictToUserMixin


class CalendarEntryListView(
    LoginRequiredMixin,
    RestrictToUserMixin,
    AllCalendarEntriesMixin,
    TemplateView,
):
    """Provide a list view of all events in a given year.

    Notes
    -----
    The :class:`~calingen.views.mixins.CalingenUserProfileIDMixin` is not really
    required, because the view fetches the (full)
    :class:`~calingen.models.profile.Profile` instance anyway. Room for
    optimization.
    """

    template_name = "calingen/calendar_entry_list_year.html"
