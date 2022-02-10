# SPDX-License-Identifier: MIT

"""Implementation of :class:`~calingen.interfaces.plugin_api.LayoutProvider` that provides different kinds of ruled paper.

This layout is HTML-based and intended to be used to generate single pages with
a given grid (*"Lineatur"*).

Warnings
--------
This layout does not include events!
"""

# local imports
from .lineatur import Lineatur  # noqa: F401

default_app_config = (
    "calingen.contrib.layouts.lineatur.apps.CalingenLayoutLineaturConfig"
)
"""The path to the app's default configuration class.

Consider this *legacy code*. See
:djangoapi:`Django's documentation<applications/#configuring-applications>` for
details.

Notes
-----
While the layout is provided as a "standalone Django app", it is in fact nothing
more than an implementation of
:class:`~calingen.interfaces.plugin_api.LayoutProvider`. The actual magic of
registering the layout with the main app is not done in this app's
:class:`~django.apps.AppConfig`, but in this very file by importing the
:class:`~calingen.contrib.layouts.lineatur.lineatur.Lineatur` class.
"""
