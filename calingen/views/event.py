# SPDX-License-Identifier: MIT

"""Provides views for the :class:`calingen.models.event.Event` model."""

# Django imports
from django.views import generic

# app imports
from calingen.models.event import Event
from calingen.views.mixins import CalingenRestrictToUserMixin


class EventDetailView(CalingenRestrictToUserMixin, generic.DetailView):
    """Provide details of a :class:`calingen.models.event.Event` instance.

    Notes
    -----
    This implementation uses Django's generic class-based view
    :class:`django.views.generic.DetailView`.
    """

    model = Event
    """Required attribute to tie this view to the model."""

    context_object_name = "event_item"
    """Provide a semantic name for the built-in context."""

    pk_url_kwarg = "event_id"
    """The name of the keyword argument as provided in the app's url configuration.

    By default, this is simply ``"pk"``, but for clarity, the app's url
    configuration (:mod:`calingen.urls`) uses the more explicit ``"event_id"``.
    """


class EventListView(CalingenRestrictToUserMixin, generic.ListView):
    """Provide a list of :class:`calingen.models.event.Event` instances.

    Notes
    -----
    This implementation uses Django's generic class-based view
    :class:`django.views.generic.ListView`.
    """

    model = Event
    """Required attribute to tie this view to the model."""

    context_object_name = "event_list"
    """Provide a semantic name for the built-in context."""
