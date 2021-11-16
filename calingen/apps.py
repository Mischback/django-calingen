# SPDX-License-Identifier: MIT

"""Provide the application configuration for Django."""

# Django imports
from django.apps import AppConfig


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

        As of now, this method does not perform anything. Anyhow, it is
        considered best practice to use this method to connect signal handlers,
        which might come in handy.
        """
        pass
