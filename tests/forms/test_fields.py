# SPDX-License-Identifier: MIT

"""Provide tests for calingen.forms.fields."""

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

    @mock.patch("calingen.forms.fields.MultiValueField")
    def test_prepare_value(self, mock_MVF):
        # Arrange (set up test environment)
        mock_ListField = mock.MagicMock()
        mock_ListField_prepare_value = mock.MagicMock()
        mock_ListField.prepare_value = mock_ListField_prepare_value
        test_value = {"unavailable": "foo"}
        a = PluginField()
        a.fields = [mock.ANY, mock_ListField]

        # Act (actually perform what has to be done)
        a.prepare_value(test_value)

        # Assert (verify the results)
        mock_ListField_prepare_value.assert_called()

    @mock.patch("calingen.forms.fields.MultiValueField")
    def test_compress_empty(self, mock_MVF):
        # Arrange (set up test environment)
        mock_ListField = mock.MagicMock()
        mock_ListField_prepare_value = mock.MagicMock()
        mock_ListField.prepare_value = mock_ListField_prepare_value
        test_value = None
        a = PluginField()

        # Act (actually perform what has to be done)
        return_value = a.compress(test_value)

        # Assert (verify the results)
        self.assertIsNone(return_value)

    @mock.patch("calingen.forms.fields.MultiValueField")
    def test_compress_valid_datalist(self, mock_MVF):
        # Arrange (set up test environment)
        mock_ListField = mock.MagicMock()
        mock_ListField_prepare_value = mock.MagicMock()
        mock_ListField.prepare_value = mock_ListField_prepare_value
        test_value = ["foo", "bar"]
        a = PluginField()

        # Act (actually perform what has to be done)
        return_value = a.compress(test_value)

        # Assert (verify the results)
        self.assertEqual(return_value["active"], "foo")
        self.assertEqual(return_value["unavailable"], "bar")
