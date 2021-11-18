# SPDX-License-Identifier: MIT

"""Integrates the app's models into Django's admin interface."""

# Django imports
from django.contrib import admin

# app imports
from calingen.models.event import Event
from calingen.models.profile import Profile


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):  # noqa: D101
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):  # noqa: D101
    pass
