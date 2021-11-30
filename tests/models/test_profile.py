# SPDX-License-Identifier: MIT

"""Provide tests for calingen.models.profile."""

# Python imports
from unittest import mock, skip  # noqa: F401

# Django imports
from django.test import override_settings, tag  # noqa: F401

# app imports
from calingen.models.profile import Profile

# local imports
from ..util.testcases import CalingenTestCase


@tag("models", "profile")
class ProfileTest(CalingenTestCase):
    @mock.patch("calingen.models.profile.EventProvider")
    def test_event_provider_getter_empty_raw(self, mock_event_provider):
        """If _event_provider is empty, return empty values."""
        # Arrange (set up test environment)
        mock_event_provider.list_available_plugins.return_value = [
            ("bar", "foo.bar"),
            ("baz", "foo.baz"),
        ]
        raw_json = {"active": [], "unavailable": []}
        profile = Profile()
        profile._event_provider = raw_json

        # Act (actually perform what has to be done)
        return_value = profile.event_provider

        # Assert (verify the results))
        self.assertEqual(return_value["active"], [])
        self.assertEqual(return_value["unavailable"], [])
        self.assertEqual(return_value["newly_unavailable"], [])

    @mock.patch("calingen.models.profile.EventProvider")
    def test_event_provider_getter_active_to_active(self, mock_event_provider):
        """Active and available stays active."""
        # Arrange (set up test environment)
        mock_event_provider.list_available_plugins.return_value = [
            ("foo.bar", "bar"),
            ("foo.baz", "baz"),
        ]
        raw_json = {"active": ["foo.bar"], "unavailable": []}
        profile = Profile()
        profile._event_provider = raw_json

        # Act (actually perform what has to be done)
        return_value = profile.event_provider

        # Assert (verify the results))
        self.assertEqual(return_value["active"], ["foo.bar"])
        self.assertEqual(return_value["unavailable"], [])
        self.assertEqual(return_value["newly_unavailable"], [])

    @mock.patch("calingen.models.profile.EventProvider")
    def test_event_provider_getter_unavailable_to_unavailable(
        self, mock_event_provider
    ):
        """Inactive and unavailable stays unavailable."""
        # Arrange (set up test environment)
        mock_event_provider.list_available_plugins.return_value = [
            ("foo.bar", "bar"),
            ("foo.baz", "baz"),
        ]
        raw_json = {"active": [], "unavailable": ["foo.bar.buhu"]}
        profile = Profile()
        profile._event_provider = raw_json

        # Act (actually perform what has to be done)
        return_value = profile.event_provider

        # Assert (verify the results))
        self.assertEqual(return_value["active"], [])
        self.assertEqual(return_value["unavailable"], ["foo.bar.buhu"])
        self.assertEqual(return_value["newly_unavailable"], [])

    @mock.patch("calingen.models.profile.EventProvider")
    def test_event_provider_getter_unavailable_to_active(self, mock_event_provider):
        """Inactive but available is moved to active."""
        # Arrange (set up test environment)
        mock_event_provider.list_available_plugins.return_value = [
            ("foo.bar", "bar"),
            ("foo.baz", "baz"),
        ]
        raw_json = {"active": ["foo.bar"], "unavailable": ["foo.baz"]}
        profile = Profile()
        profile._event_provider = raw_json

        # Act (actually perform what has to be done)
        return_value = profile.event_provider

        # Assert (verify the results))
        self.assertEqual(return_value["active"], ["foo.bar", "foo.baz"])
        self.assertEqual(return_value["unavailable"], [])
        self.assertEqual(return_value["newly_unavailable"], [])

    @mock.patch("calingen.models.profile.EventProvider")
    def test_event_provider_getter_active_to_unavailable(self, mock_event_provider):
        """Active but unavailable is moved to unavailable and included in newly_unavailable."""
        # Arrange (set up test environment)
        mock_event_provider.list_available_plugins.return_value = [
            ("foo.bar", "bar"),
            ("foo.baz", "baz"),
        ]
        raw_json = {"active": ["foo.bar.buhu"], "unavailable": []}
        profile = Profile()
        profile._event_provider = raw_json

        # Act (actually perform what has to be done)
        return_value = profile.event_provider

        # Assert (verify the results))
        self.assertEqual(return_value["active"], [])
        self.assertEqual(return_value["unavailable"], ["foo.bar.buhu"])
        self.assertEqual(return_value["newly_unavailable"], ["foo.bar.buhu"])
