# SPDX-License-Identifier: MIT

"""Provides views for the :class:`calingen.models.profile.Profile` model."""

# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.views import generic

# app imports
from calingen.models.profile import Profile
from calingen.views.mixins import CalingenInjectRequestUserIntoFormValidMixin


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

    success_url = reverse_lazy("profile-update")
    """Redirect the user to his (newly created) profile."""

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

        [describe the actual behaviour when the FIXME is fixed!]
        """
        try:
            return super().form_valid(form)
        except IntegrityError:
            # This works during manual testing, but it does not seem to be the
            # clean and usual way to go.
            # FIXME: Investigate this further!
            # - Provide a real Error, as it is best-practice in Django?
            # - simply redirect to the user's profile
            form.add_error(None, "Your profile already exists!")
            return self.form_invalid(form)
