# SPDX-License-Identifier: MIT

"""Provides app-specific URLs."""

# Python imports
import datetime

# Django imports
from django.urls import path

# app imports
from calingen.views import base, event, generation, profile, web

# see: https://docs.djangoproject.com/en/4.0/topics/http/urls/#url-namespaces
app_name = "calingen"
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
