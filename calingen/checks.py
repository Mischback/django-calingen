# SPDX-License-Identifier: MIT

"""Provide app-specific contributions to Django's check framework.

These checks validate the values of app-specific settings and may also perform
logical checks in combination with other project settings.
"""

# Django imports
from django.conf import settings
from django.core.checks import Error


def check_config_value_event_provider_notification(*args, **kwargs):
    """Verify that :attr:`~calingen.settings.CALINGEN_MISSING_EVENT_PROVIDER_NOTIFICATION` provides accepted value.

    Returns
    -------
    list
        A list of :djangodoc:`Messages <topics/checks/#messages>`.
    """
    errors = []
    config_value = settings.CALINGEN_MISSING_EVENT_PROVIDER_NOTIFICATION

    if config_value is not None:
        if config_value != "messages":
            errors.append(
                Error(
                    "Unaccepted config value for CALINGEN_MISSING_EVENT_PROVIDER_NOTIFICATIONS",
                    hint=(
                        "CALINGEN_MISSING_EVENT_PROVIDER_NOTIFICATIONS has to be "
                        'either None or "messages".'
                    ),
                    id="calingen.e001",
                )
            )

    return errors
