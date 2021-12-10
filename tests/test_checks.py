# SPDX-License-Identifier: MIT

"""Provide tests for calingen.checks."""

# Python imports
from unittest import mock, skip  # noqa: F401

# Django imports
from django.test import override_settings, tag  # noqa: F401

# app imports
from calingen.checks import check_config_value_event_provider_notification

# local imports
from .util.testcases import CalingenTestCase


@tag("checks")
class CalingenChecksTest(CalingenTestCase):
    @tag("config", "event_provider")
    def test_e001_setting_not_included(self):
        # Arrange (set up test environment)

        # Act (actually perform what has to be done)
        return_value = check_config_value_event_provider_notification(None)

        # Assert (verify the results)
        self.assertEqual(return_value, [])

    @tag("config", "event_provider")
    @override_settings(CALINGEN_MISSING_EVENT_PROVIDER_NOTIFICATION=None)
    def test_e001_setting_is_none(self):
        # Arrange (set up test environment)

        # Act (actually perform what has to be done)
        return_value = check_config_value_event_provider_notification(None)

        # Assert (verify the results)
        self.assertEqual(return_value, [])

    @tag("config", "event_provider")
    @override_settings(CALINGEN_MISSING_EVENT_PROVIDER_NOTIFICATION="messages")
    def test_e001_setting_is_valid_string(self):
        # Arrange (set up test environment)

        # Act (actually perform what has to be done)
        return_value = check_config_value_event_provider_notification(None)

        # Assert (verify the results)
        self.assertEqual(return_value, [])

    @tag("config", "event_provider")
    @override_settings(CALINGEN_MISSING_EVENT_PROVIDER_NOTIFICATION="foo")
    def test_e001_setting_is_invalid_string(self):
        # Arrange (set up test environment)

        # Act (actually perform what has to be done)
        return_value = check_config_value_event_provider_notification(None)

        # Assert (verify the results)
        self.assertNotEqual(return_value, [])
        self.assertEqual(len(return_value), 1)

    @tag("config", "event_provider")
    @override_settings(CALINGEN_MISSING_EVENT_PROVIDER_NOTIFICATION=True)
    def test_e001_setting_is_invalid_true(self):
        # Arrange (set up test environment)

        # Act (actually perform what has to be done)
        return_value = check_config_value_event_provider_notification(None)

        # Assert (verify the results)
        self.assertNotEqual(return_value, [])
        self.assertEqual(len(return_value), 1)

    @tag("config", "event_provider")
    @override_settings(CALINGEN_MISSING_EVENT_PROVIDER_NOTIFICATION=False)
    def test_e001_setting_is_invalid_false(self):
        # Arrange (set up test environment)

        # Act (actually perform what has to be done)
        return_value = check_config_value_event_provider_notification(None)

        # Assert (verify the results)
        self.assertNotEqual(return_value, [])
        self.assertEqual(len(return_value), 1)
