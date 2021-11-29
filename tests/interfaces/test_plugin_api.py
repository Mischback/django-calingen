# SPDX-License-Identifier: MIT

"""Provide tests for calingen.interfaces.plugin_api."""

# Python imports
from unittest import mock, skip  # noqa: F401

# Django imports
from django.test import override_settings, tag  # noqa: F401

# app imports
from calingen.interfaces.plugin_api import EventProvider, fully_qualified_classname

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


@tag("interfaces", "utility")
class UtilityFunctionTest(CalingenTestCase):
    def test_fully_qualified_classname_class(self):
        """fully_qualified_classname() on a class."""
        # Arrange (set up test environment)
        class EventProviderTestImplementation(EventProvider):
            pass

        a_class = EventProviderTestImplementation

        # Act (actually perform what has to be done)
        fqc = fully_qualified_classname(a_class)

        # Assert (verify the results))
        self.assertEqual(fqc, ".".join([a_class.__module__, a_class.__qualname__]))

    def test_fully_qualified_classname_instance(self):
        """fully_qualified_classname() on an instance."""
        # Arrange (set up test environment)
        class EventProviderTestImplementation(EventProvider):
            pass

        an_instance = EventProviderTestImplementation()

        # Act (actually perform what has to be done)
        fqc = fully_qualified_classname(an_instance)

        # Assert (verify the results))
        self.assertEqual(
            fqc,
            ".".join(
                [an_instance.__class__.__module__, an_instance.__class__.__qualname__]
            ),
        )
