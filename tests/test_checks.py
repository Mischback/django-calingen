# SPDX-License-Identifier: MIT

"""Provide tests for calingen.checks."""

# Python imports
from unittest import mock, skip  # noqa: F401

# Django imports
from django.test import override_settings, tag  # noqa: F401

# app imports
from calingen.checks import (
    check_config_value_compiler,
    check_config_value_event_provider_notification,
    check_session_enabled,
)

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

    @tag("config", "middleware", "sessions")
    @override_settings(MIDDLEWARE=[])
    def test_e002_missing_middleware(self):
        # Arrange (set up test environment)

        # Act (actually perform what has to be done)
        return_value = check_session_enabled(None)

        # Assert (verify the results)
        self.assertNotEqual(return_value, [])
        self.assertEqual(len(return_value), 1)

    @tag("config", "middleware", "sessions")
    @override_settings(
        MIDDLEWARE=["django.contrib.sessions.middleware.SessionMiddleware"]
    )
    def test_e002_setting_is_valid(self):
        # Arrange (set up test environment)

        # Act (actually perform what has to be done)
        return_value = check_session_enabled(None)

        # Assert (verify the results)
        self.assertEqual(return_value, [])

    @tag("config", "compiler")
    @override_settings(CALINGEN_COMPILER=None)
    def test_calingen_compiler_none(self):
        # Arrange (set up test environment)

        # Act (actually perform what has to be done)
        return_value = check_config_value_compiler(None)

        # Assert (verify the results)
        self.assertNotEqual(return_value, [])
        self.assertEqual(len(return_value), 1)
        self.assertEqual(return_value[0].id, "calingen.e003")

    @tag("config", "compiler")
    @override_settings(CALINGEN_COMPILER="foo")
    def test_calingen_compiler_string(self):
        # Arrange (set up test environment)

        # Act (actually perform what has to be done)
        return_value = check_config_value_compiler(None)

        # Assert (verify the results)
        self.assertNotEqual(return_value, [])
        self.assertEqual(len(return_value), 1)
        self.assertEqual(return_value[0].id, "calingen.e003")

    @tag("config", "compiler")
    @override_settings(CALINGEN_COMPILER={})
    def test_calingen_compiler_empty_dict(self):
        # Arrange (set up test environment)

        # Act (actually perform what has to be done)
        return_value = check_config_value_compiler(None)

        # Assert (verify the results)
        self.assertNotEqual(return_value, [])
        self.assertEqual(len(return_value), 1)
        self.assertEqual(return_value[0].id, "calingen.e003")

    @tag("config", "compiler")
    @override_settings(CALINGEN_COMPILER={"foo": "bar"})
    def test_calingen_compiler_missing_default(self):
        # Arrange (set up test environment)

        # Act (actually perform what has to be done)
        return_value = check_config_value_compiler(None)

        # Assert (verify the results)
        self.assertNotEqual(return_value, [])
        self.assertEqual(len(return_value), 1)
        self.assertEqual(return_value[0].id, "calingen.e003")

    @tag("config", "compiler")
    @override_settings(CALINGEN_COMPILER={"default": "bar"})
    @mock.patch("calingen.checks.import_string", side_effect=ImportError())
    def test_calingen_compiler_unimportable_default(self, mock_import_string):
        # Arrange (set up test environment)

        # Act (actually perform what has to be done)
        return_value = check_config_value_compiler(None)

        # Assert (verify the results)
        self.assertNotEqual(return_value, [])
        self.assertEqual(len(return_value), 1)
        self.assertEqual(return_value[0].id, "calingen.e004")

    @tag("config", "compiler")
    @override_settings(CALINGEN_COMPILER={"default": "bar"})
    @mock.patch("calingen.checks.import_string")
    def test_calingen_compiler_valid(self, mock_import_string):
        # Arrange (set up test environment)
        mock_import_string.return_value = "foo"

        # Act (actually perform what has to be done)
        return_value = check_config_value_compiler(None)

        # Assert (verify the results)
        self.assertEqual(return_value, [])
