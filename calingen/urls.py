# SPDX-License-Identifier: MIT

"""Provides app-specific URLs."""

# Django imports
from django.urls import path

# app imports
from calingen.views import event

urlpatterns = [
    path("event/", event.EventListView.as_view(), name="event-list"),
]
