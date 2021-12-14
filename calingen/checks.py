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


def check_session_enabled(*args, **kwargs):
    """Verify that :setting:`MIDDLEWARE` contains ``"django.contrib.sessions.middleware.SessionMiddleware"``.

    Returns
    -------
    list
        A list of :djangodoc:`Messages <topics/checks/#messages>`.

    Notes
    -----
    The calingen app relies on the availability of
    :djangodoc:`Sessions <topics/http/sessions/>` while processing layouts.

    This check does only verify, that Django's default Session middleware is
    active for the project. If a project substituted that middleware by a custom
    implementation, this check will fail and may be deactivated
    """
    errors = []
    if (
        "django.contrib.sessions.middleware.SessionMiddleware"
        not in settings.MIDDLEWARE
    ):
        errors.append(
            Error(
                '"SessionMiddleware" is not in "settings.MIDDLEWARE"',
                hint=(
                    "Calingen relies on Django's Sessions. It seems as the "
                    "project does not include the SessionMiddleware. "
                    "If your project relies on a custom implementation of the "
                    "SessionMiddleware, you may safely ignore this check."
                ),
                id="calingen.e002",
            )
        )

    return errors
