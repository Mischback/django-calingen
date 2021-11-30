# SPDX-License-Identifier: MIT

"""Provides basic views that are logically not connected to other components."""

# Django imports
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# app imports
from calingen.models.profile import Profile


@login_required
def homepage(request):
    """Provide the splash view for the app.

    Notes
    -----
    This is the app's main entry point, redirecting the requesting user to his
    :class:`~calingen.models.profile.Profile` (provided by
    :class:`~calingen.views.profile.ProfileUpdateView`) or to the
    :class:`~calingen.views.profile.ProfileCreateView` to create one.
    """
    # Every user has exactly one (calingen) Profile (One to One relation)
    # So, this fetches the Profile of the user or is None, if the user doesn't
    # have a Profile associated (yet)
    profile = (
        Profile.calingen_manager.get_queryset().filter_by_user(request.user).first()
    )

    # If there is no Profile, redirect to the view to add one
    if profile is None:
        return redirect("profile-add")

    # redirect to the user's Profile
    return redirect("profile", profile_id=profile.id)