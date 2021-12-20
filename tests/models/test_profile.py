# SPDX-License-Identifier: MIT

"""Provide tests for calingen.models.profile."""

# Python imports
import datetime
from unittest import mock, skip  # noqa: F401

# Django imports
from django.test import override_settings, tag  # noqa: F401

# app imports
from calingen.models.profile import Profile

# local imports
from ..util.testcases import CalingenTestCase


@tag("models", "profile")
class ProfileTest(CalingenTestCase):
    @tag("event_provider")
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

        # Assert (verify the results)
        self.assertEqual(return_value["active"], [])
        self.assertEqual(return_value["unavailable"], [])
        self.assertEqual(return_value["newly_unavailable"], [])

    @tag("event_provider")
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

        # Assert (verify the results)
        self.assertEqual(return_value["active"], ["foo.bar"])
        self.assertEqual(return_value["unavailable"], [])
        self.assertEqual(return_value["newly_unavailable"], [])

    @tag("event_provider")
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

        # Assert (verify the results)
        self.assertEqual(return_value["active"], [])
        self.assertEqual(return_value["unavailable"], ["foo.bar.buhu"])
        self.assertEqual(return_value["newly_unavailable"], [])

    @tag("event_provider")
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

        # Assert (verify the results)
        self.assertEqual(return_value["active"], ["foo.bar", "foo.baz"])
        self.assertEqual(return_value["unavailable"], [])
        self.assertEqual(return_value["newly_unavailable"], [])

    @tag("event_provider")
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

        # Assert (verify the results)
        self.assertEqual(return_value["active"], [])
        self.assertEqual(return_value["unavailable"], ["foo.bar.buhu"])
        self.assertEqual(return_value["newly_unavailable"], ["foo.bar.buhu"])

    @mock.patch("calingen.models.profile.import_string")
    @mock.patch("calingen.models.profile.CalendarEntryList")
    @mock.patch(
        "calingen.models.profile.Profile.event_provider", new_callable=mock.PropertyMock
    )
    def test_resolve_applies_given_year_in_CalenderEntry(
        self, mock_event_provider, mock_cel, mock_import_string
    ):
        """Resolving CalendarEntryList with given year."""
        # Arrange (set up test environment)
        test_active_provider = "foo.bar.buhu"
        profile = Profile()
        mock_event_provider.return_value = {"active": [test_active_provider]}

        # Act (actually perform what has to be done)
        return_value = profile.resolve(year=2020)

        # Assert (verify the results)
        mock_cel.assert_called_once()
        mock_import_string.assert_called_once_with(test_active_provider)
        mock_cel.return_value.merge.assert_called_once()
        self.assertIsInstance(return_value, mock.MagicMock)

    @mock.patch("calingen.models.profile.import_string")
    @mock.patch("calingen.models.profile.datetime")
    @mock.patch("calingen.models.profile.CalendarEntryList")
    @mock.patch(
        "calingen.models.profile.Profile.event_provider", new_callable=mock.PropertyMock
    )
    def test_resolve_applies_current_year_in_CalenderEntry(
        self, mock_event_provider, mock_cel, mock_datetime, mock_import_string
    ):
        """Resolving CalendarEntryList with current year if not specified."""
        # Arrange (set up test environment)
        test_active_provider = "foo.bar.buhu"
        profile = Profile()
        mock_event_provider.return_value = {"active": [test_active_provider]}
        mock_datetime.datetime.now.return_value = datetime.date(2020, 12, 3)

        # Act (actually perform what has to be done)
        return_value = profile.resolve()

        # Assert (verify the results)
        mock_cel.assert_called_once()
        mock_import_string.assert_called_once_with(test_active_provider)
        mock_cel.return_value.merge.assert_called_once()
        self.assertIsInstance(return_value, mock.MagicMock)
