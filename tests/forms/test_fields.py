# SPDX-License-Identifier: MIT

"""Provide tests for calingen.interfaces.plugin_api."""

# Python imports
from unittest import mock, skip  # noqa: F401

# Django imports
from django.test import override_settings, tag  # noqa: F401

# app imports
from calingen.forms.fields import CalingenListField, PluginField

# local imports
from ..util.testcases import CalingenTestCase


@tag("forms", "fields", "CalingenListField")
class CalingenListFieldTest(CalingenTestCase):
    @mock.patch("calingen.forms.fields.CharField")
    def test_to_python_empty_value(self, mock_CharField):
        """Return empty list on empty value."""
        # Arrange (set up test environment)
        list_field = CalingenListField()

        # Act (actually perform what has to be done)
        return_value = list_field.to_python(None)

        # Assert (verify the results))
        self.assertEqual([], return_value)

    @mock.patch("calingen.forms.fields.CharField")
    def test_to_python_single_value(self, mock_CharField):
        """Return list with single value."""
        # Arrange (set up test environment)
        list_field = CalingenListField()

        # Act (actually perform what has to be done)
        return_value = list_field.to_python("foo")

        # Assert (verify the results))
        self.assertEqual(["foo"], return_value)

    @mock.patch("calingen.forms.fields.CharField")
    def test_to_python_comma_seperated_values(self, mock_CharField):
        """Return list with single value."""
        # Arrange (set up test environment)
        list_field = CalingenListField()

        # Act (actually perform what has to be done)
        return_value = list_field.to_python("foo, bar")

        # Assert (verify the results))
        self.assertEqual(["foo", "bar"], return_value)


@tag("forms", "fields", "PluginField")
class PluginFieldTest(CalingenTestCase):
    @mock.patch("calingen.forms.fields.CalingenListField")
    @mock.patch("calingen.forms.fields.MultipleChoiceField")
    @mock.patch("calingen.forms.fields.MultiValueField.__new__")
    def test_constructor(self, mock_MVF, mock_MCF, mock_CLF):
        """Constructor calls the super() constructor with the specified fields."""
        # Arrange (set up test environment)
        mock_MVF_instance = mock.MagicMock()
        mock_MVF.return_value = mock_MVF_instance

        # Act (actually perform what has to be done)
        a = PluginField()  # noqa: F841

        # Assert (verify the results)
        mock_MVF.assert_called_once()
