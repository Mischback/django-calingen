# SPDX-License-Identifier: MIT

"""Provides the web views.

These views are not model-specific (see
:mod:`calingen.views.event` and :mod:`calingen.views.profile`), but provide
representations of the app's data.

Please note: The focus of calingen is to create analogous, paper-based calender
pages. These views are provided as convenience!
"""

# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

# app imports
from calingen.interfaces.data_exchange import CalenderEntryList
from calingen.models.event import Event
from calingen.models.profile import Profile
from calingen.views.mixins import (
    CalingenRestrictToUserMixin,
    CalingenUserProfileIDMixin,
)


class CalenderEntryListYearView(
    LoginRequiredMixin,
    CalingenRestrictToUserMixin,
    CalingenUserProfileIDMixin,
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

    template_name = "calingen/base_event_list_year.html"

    def get_context_data(self, **kwargs):
        """Just for linting."""
        context = super().get_context_data(**kwargs)

        # get the user's profile (required to process plugins)
        profile = Profile.calingen_manager.get_profile(self.request.user)

        all_entries = CalenderEntryList()
        internal_events = Event.calingen_manager.get_calender_entry_list(
            self.request.user
        )
        plugin_events = profile.resolve()
        all_entries.merge(internal_events)
        all_entries.merge(plugin_events)
        entries = all_entries.sorted()

        context["entries"] = entries

        return context
