# SPDX-License-Identifier: MIT

"""Provide tests for calingen.interfaces.plugin_api."""

# Python imports
from unittest import mock, skip  # noqa: F401

# Django imports
from django.test import override_settings, tag  # noqa: F401

# app imports
from calingen.interfaces.plugin_api import EventProvider

# local imports
from ..util.testcases import CalingenTestCase


@tag("interfaces", "plugin")
class EventProviderTest(CalingenTestCase):
    def test_automatic_plugin_registration(self):
        """Just verify, that the `python sorcery` as described in the source file actually works."""

        # Arrange (set up test environment)
        already_present_plugins = len(EventProvider.plugins)

        # Act (actually perform what has to be done)
        class EventProviderTestImplementation(EventProvider):
            pass

        # Assert (verify the results))
        self.assertEqual(len(EventProvider.plugins), already_present_plugins + 1)
