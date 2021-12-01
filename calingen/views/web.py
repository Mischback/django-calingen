# SPDX-License-Identifier: MIT

"""Provides the web views.

These views are not model-specific (see
:mod:`calingen.views.event` and :mod:`calingen.views.profile`), but provide
representations of the app's data.

Please note: The focus of calingen is to create analogous, paper-based calender
pages. These views are provided as convenience!
"""

# Python imports
import logging

# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

# app imports
from calingen.views.mixins import (
    CalingenRestrictToUserMixin,
    CalingenUserProfileIDMixin,
)

logger = logging.getLogger(__name__)


class EventListYearView(
    LoginRequiredMixin,
    CalingenRestrictToUserMixin,
    CalingenUserProfileIDMixin,
    TemplateView,
):
    """Provide a list view of all events in a given year."""

    template_name = "calingen/base_event_list_year.html"

    def get_context_data(self, **kwargs):
        """Just for linting."""
        context = super().get_context_data(**kwargs)

        logger.debug(context)

        return context
