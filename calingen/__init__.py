# SPDX-License-Identifier: MIT

"""A pluggable Django application to generate analogous, legacy, paper-based calendar inlays."""

__author__ = "Mischback"
"""The current project owner."""

__app_name__ = "django-calingen"
"""The name of the application."""

__version__ = "1.0.0"
"""The current version."""

default_app_config = "calingen.apps.CalingenConfig"
"""The path to the app's default configuration class.

Consider this *legacy code*. See
:djangoapi:`Django's documentation<applications/#configuring-applications>` for
details.
"""
