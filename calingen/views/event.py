# SPDX-License-Identifier: MIT

"""Provides views for the :class:`calingen.models.event.Event` model."""

# Django imports
from django.views import generic

# app imports
from calingen.models.event import Event


class EventListView(generic.ListView):
    """Provide a list of :class:`calingen.models.event.Event` instances.

    Notes
    -----
    This implementation uses Django's generic class-based view
    :class:`django.views.generic.ListView`.
    """

    model = Event
    """Required attribute to tie this view to the model."""
