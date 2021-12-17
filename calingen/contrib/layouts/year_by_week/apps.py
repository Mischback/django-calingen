# SPDX-License-Identifier: MIT

"""Provide the application configuration for Django."""

# Django imports
from django.apps import AppConfig


class CalingenLayoutYearByWeekConfig(AppConfig):
    """Application-specific configuration class, as required by Django.

    This sub-class of Django's `AppConfig` provides application-specific
    information to be used in Django's application registry (see
    :djangoapi:`applications/#configuring-applications`).
    """

    name = "calingen.contrib.layouts.year_by_week"
    verbose_name = "CalInGen Layout: Year by Week"
