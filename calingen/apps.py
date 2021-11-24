# SPDX-License-Identifier: MIT

"""Provide the application configuration for Django."""

# Python imports
import importlib
import logging

# Django imports
from django.apps import AppConfig
from django.conf import settings

# get a module-level logger
logger = logging.getLogger(__name__)


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
        # delay app imports until now, to make sure everything else is ready
        # app imports
        from calingen import settings as app_default_settings

        # inject app-specific settings
        # see https://stackoverflow.com/a/47154840
        for name in dir(app_default_settings):
            if name.isupper() and not hasattr(settings, name):
                value = getattr(app_default_settings, name)
                logger.info("Injecting setting {} with value {}".format(name, value))
                setattr(settings, name, value)

        # load the external event providers
        for provider in settings.CALINGEN_EXTERNAL_EVENT_PROVIDER:
            importlib.import_module(provider)
