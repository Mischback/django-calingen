# SPDX-License-Identifier: MIT

"""Implementation of :class:`~calingen.interfaces.plugin_api.EventProvider` that provide German holidays, splitted by federate states.

In fact, it is not only *one* implementation of
:class:`~calingen.interfaces.plugin_api.EventProvider`, but 17.

Notes
-----
The app-specific setting ``CALINGEN_PROVIDER_GERMAN_HOLIDAYS`` can be used to
filter the actually provided event providers.
"""


default_app_config = (
    "calingen.contrib.providers.german_holidays.apps.CalingenProviderGermanHolidays"
)
"""The path to the app's default configuration class.

Consider this *legacy code*. See
:djangoapi:`Django's documentation<applications/#configuring-applications>` for
details.
"""
