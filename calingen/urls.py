# SPDX-License-Identifier: MIT

"""App-specific URL configuration."""

# Python imports
import datetime

# Django imports
from django.urls import path

# app imports
from calingen.views import base, event, generation, profile, web

app_name = "calingen"
"""Define an application namespace for reversing URLs.

See :djangodoc:`URL namespaces <topics/http/urls/#url-namespaces>`.
"""

urlpatterns = [
    path("", base.homepage, name="homepage"),
    path("event/", event.EventListView.as_view(), name="event-list"),
    path("event/<int:event_id>/", event.EventDetailView.as_view(), name="event-detail"),
    path(
        "event/<int:event_id>/update/",
        event.EventUpdateView.as_view(),
        name="event-update",
    ),
    path(
        "event/<int:event_id>/delete/",
        event.EventDeleteView.as_view(),
        name="event-delete",
    ),
    path("event/add/", event.EventCreateView.as_view(), name="event-add"),
    path("<int:profile_id>/", profile.ProfileDetailView.as_view(), name="profile"),
    path("profile/add/", profile.ProfileCreateView.as_view(), name="profile-add"),
    path(
        "<int:profile_id>/delete/",
        profile.ProfileDeleteView.as_view(),
        name="profile-delete",
    ),
    path(
        "<int:profile_id>/update/",
        profile.ProfileUpdateView.as_view(),
        name="profile-update",
    ),
    path(
        "<int:profile_id>/events/",
        web.CalendarEntryListView.as_view(),
        kwargs={"target_year": datetime.datetime.now().year},
        name="calendar-entry-list-year",
    ),
    path(
        "<int:profile_id>/events/<int:target_year>/",
        web.CalendarEntryListView.as_view(),
        name="calendar-entry-list-year",
    ),
    path(
        "generate/select-layout/",
        generation.LayoutSelectionView.as_view(),
        name="layout-selection",
    ),
    path(
        "generate/configure-layout/",
        generation.LayoutConfigurationView.as_view(),
        name="layout-configuration",
    ),
    path(
        "generate/compilation/",
        generation.CompilerView.as_view(),
        name="compilation",
    ),
]
"""The actual patterns, matching URLs to views.

- ``""``: :func:`calingen.views.base.homepage` - ``"homepage"``

  The app's splash page. Will redirect to the user's profile (see
  ``"<profile_id>/"``) or to the profile creation page (see ``"profile/add/"``).
- ``"event/"``: :class:`calingen.views.event.EventListView` - ``"event-list"``

  The list of :class:`calingen.models.event.Event` instances for the requesting
  user.
- ``"event/<event_id>/"``: :class:`calingen.views.event.EventDetailView` - ``"event-detail"``

  The detailed view of an :class:`calingen.models.event.Event` instance.
- ``"event/add/"``: :class:`calingen.views.event.EventCreateView` - ``"event-add"``

  The view to create a new instance of :class:`calingen.models.event.Event`.
- ``"event/<event_id>/update/"``: :class:`calingen.views.event.EventUpdateView` - ``"event-update"``

  The view to modify / update an instance of :class:`calingen.models.event.Event`.
- ``"event/<event_id>/delete/"``: :class:`calingen.views.event.EventDeleteView` - ``"event-delete"``

  The view to delete an instance of :class:`calingen.models.event.Event`.
- ``"<profile_id>/"``: :class:`calingen.views.profile.ProfileDetailView` - ``"profile"``

  A view that summarizes the user's profile.
- ``"profile/add/"``: :class:`calingen.views.profile.ProfileCreateView` - ``"profile-add"``

  The view to create an instance of :class:`calingen.models.profile.Profile`.
- ``"<profile_id>/update/"``: :class:`calignen.views.profile.ProfileUpdateView` - ``"profile-update"``

  The view to modify / update instances of :class:`calingen.models.profile.Profile`.
- ``"<profile_id>/delete/"``: :class:`calingen.views.profile.ProfileDeleteView` - ``"profile-delete"``

  The view to delete an instance of :class:`calingen.models.profile.Profile`.
- ``"<profile_id>/events/"``: :class:`calingen.views.web.CalenderEntryListView` - ``"calendar-entry-list-year"``

  This view provides a list of a user's events. Those events are determined from
  external event providers (as configured in the user's profile) and the
  instances of :class:`calingen.models.event.Event` associated with the user.

  This view automatically determines events for the *current year*.

- ``"<profile_id>/events/<target_year>"``: :class:`calingen.views.web.CalendarEntryListView` -
  ``"calendar-entry-list-year"``

  See ``"<profile_id>/events/"``. The only difference is, that the
  ``target_year`` is provided manually through the URL.
- ``"generate/select-layout/"``: :class:`calingen.views.generation.LayoutSelectionView` - ``"layout-selection"``

  This view is the starting point of the actual *generation process*.
- ``"generate/configure-layout/"``: :class:`calingen.views.generation.LayoutConfigurationView` -
  ``"layout-configuration"``

  This view is automatically accessed during the *generation process*, if the
  selected layout requires configuration.
- ``"generate/compilation/"``: :class:`calingen.views.generation.CompilerView` - ``"compilation"``

  This view is automatically accessed during the *generation process* and
  presents the compilation result, depending on the determined compiler.
"""
