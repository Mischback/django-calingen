# SPDX-License-Identifier: MIT

"""Provide tests for calingen.models.event."""

# Python imports
import datetime
from unittest import mock, skip  # noqa: F401

# Django imports
from django.test import override_settings, tag  # noqa: F401

# app imports
from calingen.models.event import Event

# local imports
from ..util.testcases import CalingenTestCase


@tag("models", "event")
class EventTest(CalingenTestCase):
    @mock.patch("calingen.models.event.CalenderEntry")
    @mock.patch("calingen.models.event.CalenderEntryList")
    def test_resolve_applies_given_year_in_CalenderEntry(self, mock_cel, mock_ce):
        """Given year is applied to the resolved CalenderEntryList."""
        # Arrange (set up test environment)
        event = Event()
        event.title = "foo"
        event.category = "bar"
        event.start = datetime.datetime(1990, 12, 3, 0, 0)

        # Act (actually perform what has to be done)
        return_value = event.resolve(year=2020)

        # Assert (verify the results)
        mock_ce.assert_called_with("foo", "bar", datetime.date(2020, 12, 3), mock.ANY)
        self.assertIsInstance(return_value, mock.MagicMock)

    @mock.patch("calingen.models.event.datetime")
    @mock.patch("calingen.models.event.CalenderEntry")
    @mock.patch("calingen.models.event.CalenderEntryList")
    def test_resolve_applies_current_year_in_CalenderEntry(
        self, mock_cel, mock_ce, mock_datetime
    ):
        """Resolving CalenderEntryList with current year if not specified."""
        # Arrange (set up test environment)
        event = Event()
        event.title = "foo"
        event.category = "bar"
        event.start = datetime.datetime(1990, 12, 3, 0, 0)
        mock_datetime.datetime.now.return_value = datetime.date(2020, 12, 3)

        # Act (actually perform what has to be done)
        return_value = event.resolve()

        # Assert (verify the results)
        mock_ce.assert_called_with("foo", "bar", mock_datetime.date(), mock.ANY)
        self.assertIsInstance(return_value, mock.MagicMock)
