# SPDX-License-Identifier: MIT

"""Provide the application configuration for Django."""

# Django imports
from django.apps import AppConfig
from django.conf import settings

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

        It performs the following actions:

        - it checks this app's app-specific setting and performs an import of
          the required implementations of
          :class:`~calingen.interfaces.plugin_api.EventProvider`, registering
          them with the plugin mount point and thus, making them available in
          **django-calingen**.
        """
        # Provide a default value for CALINGEN_PROVIDER_GERMAN_HOLIDAYS, if not
        # present in the project's settings module
        if not hasattr(settings, APP_CONFIG_NAME):
            setattr(settings, APP_CONFIG_NAME, "all")

        app_settings = getattr(settings, APP_CONFIG_NAME)
        if app_settings == "all":
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
        else:
            if "BadenWuerttember" in app_settings:
                # local imports
                from .provider import BadenWuerttemberg  # noqa: F401
            if "Bayer" in app_settings:
                # local imports
                from .provider import Bayern  # noqa: F401
            if "Berlin" in app_settings:
                # local imports
                from .provider import Berlin  # noqa: F401
            if "Brandenburg" in app_settings:
                # local imports
                from .provider import Brandenburg  # noqa: F401
            if "Bremen" in app_settings:
                # local imports
                from .provider import Bremen  # noqa: F401
            if "Hamburg" in app_settings:
                # local imports
                from .provider import Hamburg  # noqa: F401
            if "Hessen" in app_settings:
                # local imports
                from .provider import Hessen  # noqa: F401
            if "MecklenburgVorpommern" in app_settings:
                # local imports
                from .provider import MecklenburgVorpommern  # noqa: F401
            if "Niedersachsen" in app_settings:
                # local imports
                from .provider import Niedersachsen  # noqa: F401
            if "NordrheinWestphalen" in app_settings:
                # local imports
                from .provider import NordrheinWestphalen  # noqa: F401
            if "RheinlandPfalz" in app_settings:
                # local imports
                from .provider import RheinlandPfalz  # noqa: F401
            if "Saarland" in app_settings:
                # local imports
                from .provider import Saarland  # noqa: F401
            if "Sachsen" in app_settings:
                # local imports
                from .provider import Sachsen  # noqa: F401
            if "SachsenAnhalt" in app_settings:
                # local imports
                from .provider import SachsenAnhalt  # noqa: F401
            if "SchleswigHolstein" in app_settings:
                # local imports
                from .provider import SchleswigHolstein  # noqa: F401
            if "Thueringen" in app_settings:
                # local imports
                from .provider import Thueringen  # noqa: F401
