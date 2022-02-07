# SPDX-License-Identifier: MIT

"""Implementation of :class:`~calingen.interfaces.plugin_api.LayoutProvider` that provides TeX-sources for a simple list of events."""

# local imports
from .simple_event_list import SimpleEventList  # noqa: F401

default_app_config = "calingen.contrib.layouts.simple_event_list.apps.CalingenLayoutSimpleEventListConfig"
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
:class:`~calingen.contrib.layouts.simple_event_list.simple_event_list.SimpleEventList`
class.
"""
