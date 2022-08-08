# SPDX-License-Identifier: MIT

"""Provide tests for calingen.models.event."""

# Python imports
import datetime
from unittest import mock, skip  # noqa: F401

# Django imports
from django.contrib.auth.models import User
from django.test import override_settings, tag  # noqa: F401

# app imports
from calingen.models.event import Event, EventModelException, EventQuerySet

# local imports
from ..util.testcases import CalingenORMTestCase, CalingenTestCase


@tag("models", "event", "EventQuerySet")
class EventQuerySetTest(CalingenORMTestCase):
    def test_filter_by_user(self):
        # Arrange (set up test environment)
        alice = User.objects.get(pk=2)  # Alice!
        alice_events = Event.objects.filter(profile__owner=alice).all()
        bob = User.objects.get(pk=3)  # Bob!
        bob_events = Event.objects.filter(profile__owner=bob).all()

        # Act (actually perform what has to be done)
        test_alice_events = EventQuerySet(Event).filter_by_user(alice)
        test_bob_events = EventQuerySet(Event).filter_by_user(bob)

        self.maxDiff = None

        # Assert (verify the results)
        self.assertQuerysetEqual(
            alice_events, map(repr, test_alice_events), ordered=False, transform=repr
        )
        self.assertQuerysetEqual(
            bob_events, map(repr, test_bob_events), ordered=False, transform=repr
        )


@tag("models", "event", "EventManager")
class EventManagerTest(CalingenORMTestCase):
    def test_get_user_events_qs(self):
        # Arrange (set up test environment)
        alice = User.objects.get(pk=2)  # Alice!
        alice_events = Event.objects.filter(profile__owner=alice).all()
        bob = User.objects.get(pk=3)  # Bob!
        bob_events = Event.objects.filter(profile__owner=bob).all()

        # Act (actually perform what has to be done)
        test_alice_events = Event.calingen_manager.get_user_events_qs(user=alice)
        test_bob_events = Event.calingen_manager.get_user_events_qs(user=bob)

        # Assert (verify the results)
        self.assertQuerysetEqual(
            alice_events, map(repr, test_alice_events), ordered=False, transform=repr
        )
        self.assertQuerysetEqual(
            bob_events, map(repr, test_bob_events), ordered=False, transform=repr
        )

    def test_get_user_events_qs_exception(self):
        # Arrange (set up test environment)

        # Act (actually perform what has to be done)
        # Assert (verify the results)
        with self.assertRaises(EventModelException):
            test_alice_events = (  # noqa: F841
                Event.calingen_manager.get_user_events_qs()
            )

    def test_summary(self):
        # Arrange (set up test environment)
        alice = User.objects.get(pk=2)  # Alice!
        alice_events = Event.objects.filter(profile__owner=alice).count()

        # Act (actually perform what has to be done)
        test_alice_events = Event.calingen_manager.summary(user=alice)

        # Assert (verify the results)
        self.assertEqual(alice_events, test_alice_events)

    @mock.patch("calingen.models.event.CalendarEntryList")
    def test_get_calendar_entry_list(self, mock_calendarentrylist):
        # Arrange (set up test environment)
        mock_merge = mock.MagicMock()
        mock_calendarentrylist.return_value.merge = mock_merge
        alice = User.objects.get(pk=2)  # Alice!
        alice_events = Event.objects.filter(profile__owner=alice).count()

        # Act (actually perform what has to be done)
        test_alice_events = (  # noqa: F841
            Event.calingen_manager.get_calendar_entry_list(user=alice)
        )

        # Assert (verify the results)
        self.assertEqual(mock_merge.call_count, alice_events)


@tag("models", "event", "Event")
class EventTest(CalingenTestCase):
    @mock.patch("calingen.models.event.CalendarEntry")
    @mock.patch("calingen.models.event.CalendarEntryList")
    def test_resolve_applies_given_year_in_CalendarEntry(self, mock_cel, mock_ce):
        """Given year is applied to the resolved CalendarEntryList."""
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
    @mock.patch("calingen.models.event.CalendarEntry")
    @mock.patch("calingen.models.event.CalendarEntryList")
    def test_resolve_applies_current_year_in_CalendarEntry(
        self, mock_cel, mock_ce, mock_datetime
    ):
        """Resolving CalendarEntryList with current year if not specified."""
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
