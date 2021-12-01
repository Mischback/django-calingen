# SPDX-License-Identifier: MIT

"""Provides views for the :class:`calingen.models.event.Event` model."""

# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

# app imports
from calingen.models.event import Event, EventForm
from calingen.models.profile import Profile
from calingen.views.mixins import CalingenRestrictToUserMixin


class EventCreateView(LoginRequiredMixin, generic.CreateView):
    """Provide the generic class-based view implementation to add `Event` objects.

    Notes
    -----
    This implementation uses Django's generic class-based view
    :class:`django.views.generic.CreateView`.

    The view relies on :class:`calingen.models.event.EventForm` as its
    ``ModelForm``. This is required to make custom validation logic available.
    """

    model = Event
    """Required attribute to tie this view to the model."""

    form_class = EventForm
    """Specify which form to use."""

    template_name_suffix = "_create"
    """Make the view use the template ``calingen/event_create.html``."""

    def form_valid(self, form):
        """Inject the user's :class:`~calingen.models.profile.Profile` into the form.

        Every user does have only one :class:`~calingen.models.profile.Profile`
        and :class:`~calingen.models.event.Event` instances are directly tied
        to that ``Profile``.

        The :class:`~calingen.models.event.EventForm`` does not include the
        field to select the ``Profile``, as user's are only allowed to create
        ``Event`` instances for themselves.

        This method `injects` the user's ``Profile`` into the ``form.instance``
        to maintain database integrity.
        """
        # get the user's Profile to inject this into the instance
        form.instance.profile = Profile.objects.get(owner=self.request.user)

        return super().form_valid(form)


class EventDeleteView(
    CalingenRestrictToUserMixin, LoginRequiredMixin, generic.DeleteView
):
    """Provide the generic class-based view implementation to delete `Event` objects.

    Notes
    -----
    This implementation uses Django's generic class-based view
    :class:`django.views.generic.DeleteView`.
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

    success_url = reverse_lazy("event-list")
    """The URL to redirect to after successfully deleting the instance."""


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


class EventUpdateView(
    CalingenRestrictToUserMixin, LoginRequiredMixin, generic.UpdateView
):
    """Provide the generic class-based view implementation to update `Event` objects.

    Notes
    -----
    This implementation uses Django's generic class-based view
    :class:`django.views.generic.UpdateView`.

    The view relies on :class:`calingen.models.event.EventForm` as its
    ``ModelForm``. This is required to make custom validation logic available.
    """

    model = Event
    """Required attribute to tie this view to the model."""

    form_class = EventForm
    """Specify which form to use."""

    pk_url_kwarg = "event_id"
    """The name of the keyword argument as provided in the app's url configuration.

    By default, this is simply ``"pk"``, but for clarity, the app's url
    configuration (:mod:`calingen.urls`) uses the more explicit ``"event_id"``.
    """

    template_name_suffix = "_update"
    """Make the view use the template ``calingen/event_update.html``."""
