# SPDX-License-Identifier: MIT

"""Provides views for the :class:`calingen.models.event.Event` model."""

# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

# app imports
from calingen.models.event import Event
from calingen.views.mixins import CalingenRestrictToUserMixin


class EventCreateView(LoginRequiredMixin, generic.CreateView):
    """Provide the generic class-based view implementation to add `Event` objects.

    Notes
    -----
    This implementation uses Django's generic class-based view
    :class:`django.views.generic.CreateView`.

    As of now, the automatically generated ``ModelForm`` is used. This might be
    subject to changes, as the generated form might not be sufficient to support
    the complexer details of the :class:`calingen.models.event.Event` model.
    """

    model = Event
    """Required attribute to tie this view to the model."""

    fields = ["title", "start", "type"]
    """Required attribute to make the generic ``ModelForm`` work."""

    def form_valid(self, form):
        """Override of the default ``form_valid`` method.

        Notes
        -----
        This override enables the ``form`` to automatically tie the
        :class:`calingen.models.event.Event` instance to be created to the
        ``request.user``, applying him automatically as value for
        :attr:`calingen.models.event.Event.owner` (see
        :djangodoc:`topics/class-based-views/generic-editing/#models-and-request-user`).
        """
        form.instance.owner = self.request.user
        return super().form_valid(form)


class EventDetailView(
    CalingenRestrictToUserMixin, LoginRequiredMixin, generic.DetailView
):
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


class EventListView(CalingenRestrictToUserMixin, LoginRequiredMixin, generic.ListView):
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
