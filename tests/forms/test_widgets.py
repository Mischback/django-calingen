# SPDX-License-Identifier: MIT

"""Provide tests for calingen.forms.widgets."""

# Python imports
from unittest import mock, skip  # noqa: F401

# Django imports
from django.test import override_settings, tag  # noqa: F401

# app imports
from calingen.forms.widgets import PluginWidget

# local imports
from ..util.testcases import CalingenTestCase


@tag("forms", "widgets", "PluginWidget")
class PluginWidgetTest(CalingenTestCase):
    @mock.patch("calingen.forms.widgets.MultiWidget")
    def test_decompress_empty(self, mock_MultiWidget):
        """Expand None to both values."""
        # Arrange (set up test environment)
        widget = PluginWidget()

        # Act (actually perform what has to be done)
        return_value = widget.decompress(None)

        # Assert (verify the results)
        self.assertEqual(return_value, [None, None])

    @mock.patch("calingen.forms.widgets.MultiWidget")
    def test_decompress_only_active(self, mock_MultiWidget):
        """Provide empty list for unavailable."""
        # Arrange (set up test environment)
        widget = PluginWidget()
        test_value = {"active": "foo"}

        # Act (actually perform what has to be done)
        return_value = widget.decompress(test_value)

        # Assert (verify the results)
        self.assertEqual(return_value, ["foo", []])

    @mock.patch("calingen.forms.widgets.MultiWidget")
    def test_decompress_only_unavailable(self, mock_MultiWidget):
        """Provide empty list for active."""
        # Arrange (set up test environment)
        widget = PluginWidget()
        test_value = {"unavailable": "foo"}

        # Act (actually perform what has to be done)
        return_value = widget.decompress(test_value)

        # Assert (verify the results)
        self.assertEqual(return_value, [[], "foo"])

    @mock.patch("calingen.forms.widgets.MultiWidget")
    def test_decompress(self, mock_MultiWidget):
        """Normal operation for expected structure of value."""
        # Arrange (set up test environment)
        widget = PluginWidget()
        test_value = {"active": "foo", "unavailable": "bar"}

        # Act (actually perform what has to be done)
        return_value = widget.decompress(test_value)

        # Assert (verify the results)
        self.assertEqual(return_value, ["foo", "bar"])
