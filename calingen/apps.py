# SPDX-License-Identifier: MIT

"""Provide the application configuration for Django."""

# Python imports
import importlib

# Django imports
from django.apps import AppConfig
from django.conf import settings


class CalingenConfig(AppConfig):
    """Application-specific configuration class, as required by Django.

    This sub-class of Django's `AppConfig` provides application-specific
    information to be used in Django's application registry (see
    :djangoapi:`applications/#configuring-applications`).
    """

    name = "calingen"
    verbose_name = "CalInGen"

    def ready(self) -> None:
        """Apply app-specific stuff.

        Notes
        -----
        This method is executed when the application is (completely) loaded.
        """
        # load the external event providers
        for provider in settings.CALINGEN_EXTERNAL_EVENT_PROVIDER:
            importlib.import_module(provider)
