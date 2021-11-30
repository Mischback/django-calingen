# SPDX-License-Identifier: MIT

"""Provides views for the :class:`calingen.models.profile.Profile` model."""

# Django imports
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

# app imports
from calingen.models.event import Event
from calingen.models.profile import Profile, ProfileForm
from calingen.views.mixins import (
    CalingenInjectRequestUserIntoFormValidMixin,
    CalingenRestrictToUserMixin,
)


class ProfileView(
    LoginRequiredMixin, CalingenRestrictToUserMixin, generic.base.TemplateView
):
    """Just for linting."""

    template_name = "calingen/profile.html"

    def get_context_data(self, **kwargs):
        """Just for linting."""
        context = super().get_context_data(**kwargs)

        # add summary of Event instances and EventProvider instances
        user_events = Event.calingen_manager.summary(self.request.user)
        # provider_events = len(
        #     resolve_event_provider(context["profile"].event_provider["active"])._entries
        # )
        context["events"] = {
            "user_provided": user_events,
            # "external_provider": provider_events,
        }

        return context


class ProfileCreateView(
    LoginRequiredMixin, CalingenInjectRequestUserIntoFormValidMixin, generic.CreateView
):
    """Provide the generic class-based view implementation to add `Profile` objects.

    Notes
    -----
    This implementation uses Django's generic class-based view
    :class:`django.views.generic.CreateView`.
    """

    model = Profile
    """Required attribute to tie this view to the model."""

    fields = []
    """The fields to include into the form.

    This list is left empty, as the creation of the
    :class:`~calingen.models.profile.Profile` instance is a one-off operation,
    simply tying the instance to an existing ``User`` of the Django project.
    """

    template_name_suffix = "_create"
    """Make the view use the template ``calingen/profile_create.html``."""

    def form_valid(self, form):
        """Handle database integrity errors.

        Notes
        -----
        The view relies on an automatically generated instance of Django's
        :class:`~django.forms.ModelForm` **without** any fields. Thus,
        validation of the ``form`` is a given, as the ``request.user`` is
        injected **after** form validation.

        However, the :class:`~calingen.models.profile.Profile` has a 1:1 relation
        with the project's :setting:`AUTH_USER_MODEL`, so trying to create
        multiple instances of :class:`~calingen.models.profile.Profile` for the
        same `user` will raise an :class:`~django.db.IntegrityError`.

        If the :class:`~django.db.IntegrityError` is catched, the user will be
        redirected to his profile page.
        """
        try:
            return super().form_valid(form)
        except IntegrityError:
            # The requesting user already has a profile, simply redirect him
            return redirect("profile", self.request.user.id)


class ProfileDeleteView(
    LoginRequiredMixin, CalingenRestrictToUserMixin, generic.DeleteView
):
    """Provide the generic class-based view implementation to delete `Profile` objects.

    Notes
    -----
    This implementation uses Django's generic class-based view
    :class:`django.views.generic.DeleteView`.
    """

    model = Profile
    """Required attribute to tie this view to the model."""

    context_object_name = "profile_item"
    """Provide a semantic name for the built-in context."""

    pk_url_kwarg = "profile_id"
    """The name of the keyword argument as provided in the app's url configuration.

    By default, this is simply ``"pk"``, but for clarity, the app's url
    configuration (:mod:`calingen.urls`) uses the more explicit ``"profile_id"``.
    """

    success_url = reverse_lazy("profile-add")
    """The URL to redirect to after successfully deleting the instance.

    Warnings
    --------
    As of now, this redirect to the page to create a profile. This **must** be
    adjusted, once the `real` estimated flows are implemented with all required
    views.
    """


class ProfileUpdateView(
    CalingenRestrictToUserMixin, LoginRequiredMixin, generic.UpdateView
):
    """Provide the generic class-based view implementation to add `Profile` objects.

    Notes
    -----
    This implementation uses Django's generic class-based view
    :class:`django.views.generic.CreateView`.
    """

    model = Profile
    """Required attribute to tie this view to the model."""

    form_class = ProfileForm
    """Specify which form to use."""

    pk_url_kwarg = "profile_id"
    """The name of the keyword argument as provided in the app's url configuration.

    By default, this is simply ``"pk"``, but for clarity, the app's url
    configuration (:mod:`calingen.urls`) uses the more explicit ``"profile_id"``.
    """

    template_name_suffix = "_update"
    """Make the view use the template ``calingen/profile_update.html``."""

    def get_context_data(self, **kwargs):
        """Provide additional context for this view, depending on app-specific settings.

        While accessing the users :class:`~calingen.models.profile.Profile`,
        its list of ``event_provider`` is updated. If there are providers, that
        are moved from ``active`` to ``unavailable``, the user is informed using
        Django's ``messages`` framework.

        This is dependent on the setting
        :attr:`~calingen.settings.CALINGEN_MISSING_EVENT_PROVIDER_NOTIFICATION`.
        """
        if settings.CALINGEN_MISSING_EVENT_PROVIDER_NOTIFICATION == "messages":
            # get the context
            context = super().get_context_data(**kwargs)

            # evaluate, if there are newly deactivated plugins and add a message
            for deactivated_plugin in context["profile"].event_provider[
                "newly_unavailable"
            ]:
                messages.warning(
                    self.request,
                    "The following plugin is no longer available: {}".format(
                        deactivated_plugin
                    ),
                    fail_silently=True,
                )

            return context

        return super().get_context_data(**kwargs)
