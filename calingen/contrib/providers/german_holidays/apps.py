# SPDX-License-Identifier: MIT

"""Provide the application configuration for Django."""

# Django imports
from django.apps import AppConfig

APP_CONFIG_NAME = "CALINGEN_PROVIDER_GERMAN_HOLIDAYS"
"""The name of the app-specific configuration option."""


class CalingenProviderGermanHolidays(AppConfig):
    """Application-specific configuration class, as required by Django.

    This sub-class of Django's `AppConfig` provides application-specific
    information to be used in Django's application registry (see
    :djangoapi:`applications/#configuring-applications`).
    """

    name = "calingen.contrib.providers.german_holidays"
    verbose_name = "CalInGen Provider: German Holidays"

    def ready(self):
        """Apply app-specific stuff.

        Notes
        -----
        This method is executed when the application is (completely) loaded.

        It will import the actual implementations of
        :class:`~calingen.interfaces.plugin_api.EventProvider`, making them
        available in **django-calingen**.
        """
        # local imports
        from .provider import (  # noqa: F401
            BadenWuerttemberg,
            Bayern,
            Berlin,
            Brandenburg,
            Bremen,
            GermanyFederal,
            Hamburg,
            Hessen,
            MecklenburgVorpommern,
            Niedersachsen,
            NordrheinWestphalen,
            RheinlandPfalz,
            Saarland,
            Sachsen,
            SachsenAnhalt,
            SchleswigHolstein,
            Thueringen,
        )
