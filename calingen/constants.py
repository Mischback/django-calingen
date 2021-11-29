# SPDX-License-Identifier: MIT

"""App-specific constants, that are used throughout the application."""

# Django imports
from django.db.models import TextChoices
from django.utils.translation import ugettext_lazy as _


class EventType(TextChoices):
    """The single source of truth for different types of events.

    Throughout the app, there are different sources for events, most notably the
    app's :class:`~calingen.models.event.Event` instances and the events as
    provided by the :class:`~calingen.interfaces.plugin_api.EventProvider`
    implementations.

    All these sources **must** provide compatible event types.

    Notes
    -----
    Provides the accepted choices for :attr:`calingen.models.event.Event.type`.
    """

    ANNUAL_ANNIVERSARY = "ANNUAL_ANNIVERSARY", _("Annual Anniversary")
    HOLIDAY = "HOLIDAY", _("Holiday")