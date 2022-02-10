# SPDX-License-Identifier: MIT

"""Provides the app's utility configuration to be run without Django project.

The utility configuration is used to facilitate the development of the app
without using a parent Django project and is used in tox's configuration
(see pyproject.toml -> [tool.tox] -> [testenv:django]).
"""

# Django imports
from django.conf import settings


def callback_show_debug_toolbar(request):
    """Return ``settings.DEBUG`` to control debug_toolbar."""
    return settings.DEBUG
