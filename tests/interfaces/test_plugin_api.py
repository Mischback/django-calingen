# SPDX-License-Identifier: MIT

"""Provide tests for calingen.interfaces.plugin_api."""

# Python imports
from unittest import mock, skip  # noqa: F401

# Django imports
from django.test import override_settings, tag  # noqa: F401
from django.utils.functional import classproperty

# app imports
from calingen.interfaces.plugin_api import (
    EventProvider,
    LayoutProvider,
    fully_qualified_classname,
)

# local imports
from ..util.testcases import CalingenTestCase


@tag("interfaces", "plugin", "EventProvider")
class EventProviderTest(CalingenTestCase):
    def test_automatic_plugin_registration(self):
        """Just verify, that the `python sorcery` as described in the source file actually works."""

        # Arrange (set up test environment)
        already_present_plugins = len(EventProvider.plugins)

        # Act (actually perform what has to be done)
        class EventProviderTestImplementation(EventProvider):
            title = "do-not-care"

        # Assert (verify the results)
        self.assertEqual(len(EventProvider.plugins), already_present_plugins + 1)

    def test_list_available_plugins(self):
        """Verify that EventProvider instances are listed."""

        # Arrange (set up test environment)
        test_implementation_name = "TestImplementation"

        class EventProviderTestImplementation_list_plugins_test(EventProvider):
            title = test_implementation_name

        # Act (actually perform what has to be done)
        event_provider_list = EventProvider.list_available_plugins()

        # Assert (verify the results)
        self.assertIn((mock.ANY, test_implementation_name), event_provider_list)


@tag("interfaces", "plugin", "LayoutProvider")
class LayoutProviderTest(CalingenTestCase):
    def test_automatic_plugin_registration(self):
        """Just verify, that the `python sorcery` as described in the source file actually works."""

        # Arrange (set up test environment)
        already_present_plugins = len(LayoutProvider.plugins)

        # Act (actually perform what has to be done)
        class LayoutProviderTestImplementation(LayoutProvider):
            name = "do-not-care"
            paper_size = "foo"
            orientation = "bar"

        # Assert (verify the results)
        self.assertEqual(len(LayoutProvider.plugins), already_present_plugins + 1)

    def test_title_classattribute(self):
        # Arrange (set up test environment)
        test_name = "do-not-care"
        test_paper = "foo"
        test_orientation = "bar"

        class LayoutProviderTestImplementation(LayoutProvider):
            name = test_name
            paper_size = test_paper
            orientation = test_orientation

        # Act (actually perform what has to be done)

        # Assert (verify the results)
        self.assertEqual(
            LayoutProviderTestImplementation.title,
            "{} ({}, {})".format(test_name, test_paper, test_orientation),
        )

    def test_list_available_plugins(self):
        """Verify that LayoutProvider instances are listed."""

        # Arrange (set up test environment)
        test_implementation_title = "TestImplementation"

        class LayoutProviderTestImplementation_list_plugins_test(LayoutProvider):
            @classproperty
            def title(cls):
                return test_implementation_title

        # Act (actually perform what has to be done)
        layout_provider_list = LayoutProvider.list_available_plugins()

        # Assert (verify the results)
        self.assertIn((mock.ANY, test_implementation_title), layout_provider_list)

    @mock.patch("calingen.interfaces.plugin_api.render_to_string")
    def test_render(self, mock_render_to_string):
        # Arrange (set up test environment)
        test_context = mock.MagicMock()
        mock_render_to_string.return_value = "foo"
        test_template = mock.ANY

        class LayoutProviderTestImplementation(LayoutProvider):
            name = "do-not-care"
            paper_size = "foo"
            orientation = "bar"
            _template = test_template

        # Act (actually perform what has to be done)
        render_result = LayoutProviderTestImplementation.render(test_context)

        # Assert (verify the results)
        self.assertEqual(render_result, "foo")
        mock_render_to_string.assert_called_once_with(test_template, test_context)


@tag("interfaces", "utility")
class UtilityFunctionTest(CalingenTestCase):
    def test_fully_qualified_classname_class(self):
        """fully_qualified_classname() on a class."""
        # Arrange (set up test environment)
        class EventProviderTestImplementation(EventProvider):
            title = "do-not-care"

        a_class = EventProviderTestImplementation

        # Act (actually perform what has to be done)
        fqc = fully_qualified_classname(a_class)

        # Assert (verify the results)
        self.assertEqual(fqc, ".".join([a_class.__module__, a_class.__qualname__]))

    def test_fully_qualified_classname_instance(self):
        """fully_qualified_classname() on an instance."""
        # Arrange (set up test environment)
        class EventProviderTestImplementation(EventProvider):
            title = "do-not-care"

        an_instance = EventProviderTestImplementation()

        # Act (actually perform what has to be done)
        fqc = fully_qualified_classname(an_instance)

        # Assert (verify the results)
        self.assertEqual(
            fqc,
            ".".join(
                [an_instance.__class__.__module__, an_instance.__class__.__qualname__]
            ),
        )
