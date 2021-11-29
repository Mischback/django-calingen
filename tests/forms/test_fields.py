# SPDX-License-Identifier: MIT

"""Provide tests for calingen.interfaces.plugin_api."""

# Python imports
from unittest import mock, skip  # noqa: F401

# Django imports
from django.test import override_settings, tag  # noqa: F401

# app imports
from calingen.forms.fields import CalingenListField

# local imports
from ..util.testcases import CalingenTestCase


@tag("forms", "fields", "CalingenListField")
class CalingenListFieldTest(CalingenTestCase):
    def test_to_python_empty_value(self):
        """Return empty list on empty value."""
        # Arrange (set up test environment)
        list_field = CalingenListField()

        # Act (actually perform what has to be done)
        return_value = list_field.to_python(None)

        # Assert (verify the results))
        self.assertEqual([], return_value)

    def test_to_python_single_value(self):
        """Return list with single value."""
        # Arrange (set up test environment)
        list_field = CalingenListField()

        # Act (actually perform what has to be done)
        return_value = list_field.to_python("foo")

        # Assert (verify the results))
        self.assertEqual(["foo"], return_value)

    def test_to_python_comma_seperated_values(self):
        """Return list with single value."""
        # Arrange (set up test environment)
        list_field = CalingenListField()

        # Act (actually perform what has to be done)
        return_value = list_field.to_python("foo, bar")

        # Assert (verify the results))
        self.assertEqual(["foo", "bar"], return_value)
