# SPDX-License-Identifier: MIT

"""App-specific contributions to :djangodoc:`Django's System check framework <topics/checks/>`.

These checks validate the values of app-specific settings and may also perform
logical checks in combination with other project settings.
"""

# Django imports
from django.conf import settings
from django.core.checks import Error
from django.utils.module_loading import import_string


def check_config_value_event_provider_notification(*args, **kwargs):
    """Verify that :attr:`~calingen.settings.CALINGEN_MISSING_EVENT_PROVIDER_NOTIFICATION` provides accepted value.

    - **Check ID**: ``calingen.e001``

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

    - **Check ID**: ``calingen.e002``

    Returns
    -------
    list
        A list of :djangodoc:`Messages <topics/checks/#messages>`.

    Notes
    -----
    The calingen app relies on the availability of
    :djangodoc:`Sessions <topics/http/sessions/>` while processing layouts.

    This check does only verify that Django's default Session middleware is
    active for the project. If a project substituted that middleware by a custom
    implementation, this check will fail and may be deactivated.
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


def check_config_value_compiler(*args, **kwargs):
    """Validate :attr:`~calingen.settings.CALINGEN_COMPILER` setting.

    - **Check ID**: ``calingen.e003`` - default compiler missing
    - **Check ID**: ``calingen.e004`` - default compiler not importable

    Returns
    -------
    list
        A list of :djangodoc:`Messages <topics/checks/#messages>`.

    Warnings
    --------
    This check does not verify the importability *(is this a word?)* of all
    configured compilers. It just ensures the presence of the ``"default"``
    compiler and its importability.

    Notes
    -----
    :attr:`~calingen.settings.CALINGEN_COMPILER` is a required configuration
    value and **must** be provided in the project's settings module. It is
    injected with a sane default value, if not provided.

    This check ensures, that ``CALINGEN_COMPILER["default"]`` is provided and
    that the provided compiler (instance of
    :class:`calingen.interfaces.plugin_api.CompilerProvider`) is importable.
    """
    errors = []
    config_value = settings.CALINGEN_COMPILER

    try:
        temp = config_value["default"]
    except (KeyError, TypeError):
        errors.append(
            Error(
                '"CALINGEN_COMPILER" does not provide a "default" compiler',
                hint=(
                    "CALINGEN_COMPILER must provide a default compiler. It is "
                    "recommended to use a compiler that can handle all types "
                    "of layouts."
                ),
                id="calingen.e003",
            )
        )
        return errors

    try:
        import_string(temp)
    except ImportError:
        errors.append(
            Error(
                'CALINGEN_COMPILER["default"] could not be imported',
                hint=(
                    "The specified compiler could not be imported. Make sure "
                    "to provide a full dotted Python path to the compiler "
                    "implementation."
                ),
                id="calingen.e004",
            )
        )

    return errors
