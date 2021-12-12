# SPDX-License-Identifier: MIT

"""Provide tests for calingen.interfaces.data_exchange."""

# Python imports
import datetime
from unittest import mock, skip  # noqa: F401

# Django imports
from django.test import override_settings, tag  # noqa: F401

# external imports
from dateutil import parser

# app imports
from calingen.interfaces.data_exchange import CalenderEntry, CalenderEntryList

# local imports
from ..util.testcases import CalingenTestCase


@tag("interfaces", "data", "calenderentry")
class CalenderEntryTest(CalingenTestCase):
    """Provide tests for the CalenderEntry class."""

    def test_constructor_accepts_datetime(self):
        # Arrange (set up test environment)
        test_datetime = datetime.datetime(2021, 12, 2, 14, 48)

        # Act (actually perform what has to be done)
        entry = CalenderEntry("foo", "bar", test_datetime, ("foo", "bar"))

        # Assert (verify the results)
        self.assertEqual(entry.timestamp, test_datetime, ("foo", "bar"))

    def test_constructor_accepts_date(self):
        # Arrange (set up test environment)
        test_date = datetime.date(2021, 12, 2)

        # Act (actually perform what has to be done)
        entry = CalenderEntry("foo", "bar", test_date, ("foo", "bar"))

        # Assert (verify the results)
        self.assertEqual(entry.timestamp.date(), test_date)
        self.assertEqual(entry.timestamp.time(), datetime.time.min)

    def test_constructor_accepts_datestring(self):
        # Arrange (set up test environment)
        test_datetime = datetime.datetime(2021, 12, 2, 14, 48)
        test_datetime_str = test_datetime.__str__()

        # Act (actually perform what has to be done)
        entry = CalenderEntry("foo", "bar", test_datetime_str, ("foo", "bar"))

        # Assert (verify the results)
        self.assertEqual(entry.timestamp, test_datetime)

    def test_constructor_rejects_non_valid_timestamp(self):
        # Arrange (set up test environment)
        test_datetime_str = "foobar"

        # Act (actually perform what has to be done)
        # Assert (verify the results)
        with self.assertRaises(parser._parser.ParserError):
            entry = CalenderEntry(  # noqa: F841
                "foo", "bar", test_datetime_str, ("foo", "bar")
            )

    def test_constructor_rejects_non_valid_source(self):
        # Arrange (set up test environment)
        test_date = datetime.date(2021, 12, 2)

        # Act (actually perform what has to be done)
        # Assert (verify the results)
        with self.assertRaises(CalenderEntry.CalenderEntryException):
            entry = CalenderEntry("foo", "bar", test_date, "BREAK")  # noqa: F841

    @mock.patch("calingen.interfaces.data_exchange.EventCategory")
    def test_constructor_accepts_event_category(self, mock_event_category):
        # Arrange (set up test environment)
        test_datetime = datetime.datetime(2021, 12, 12, 8, 15)
        test_category = "TEST_CAT"
        test_event_cat = mock.MagicMock()
        mock_event_category.__getitem__.return_value = test_event_cat
        mock_event_category.values = [test_category]

        # Act (actually perform what has to be done)
        entry = CalenderEntry("foo", test_category, test_datetime, ("foo", "bar"))

        # Assert (verify the results)
        self.assertEqual(entry.timestamp, test_datetime)
        self.assertEqual(entry.category, test_event_cat)

    def test_eq_different_classes(self):
        # Arrange (set up test environment)
        class TestClass:
            pass

        test_class = TestClass()
        entry = CalenderEntry(
            "foo", "bar", datetime.datetime(2021, 12, 2, 15, 4), ("foo", "bar")
        )

        # Act (actually perform what has to be done)
        return_value = entry.__eq__(test_class)

        # Assert (verify the results)
        self.assertEqual(return_value, NotImplemented)
        self.assertNotEqual(entry, test_class)
        self.assertNotEqual(test_class, entry)

    def test_lt_different_classes(self):
        # Arrange (set up test environment)
        class TestClass:
            pass

        test_class = TestClass()
        entry = CalenderEntry(
            "foo", "bar", datetime.datetime(2021, 12, 2, 15, 4), ("foo", "bar")
        )

        # Act (actually perform what has to be done)
        return_value = entry.__lt__(test_class)

        # Assert (verify the results)
        self.assertEqual(return_value, NotImplemented)

        with self.assertRaises(TypeError):
            self.assertLess(entry, test_class)

    def test_lt_timestamp(self):
        # Arrange (set up test environment)
        entry_1 = CalenderEntry(
            "aaa", "bbb", datetime.datetime(2021, 12, 2, 15, 4), ("foo", "bar")
        )
        entry_2 = CalenderEntry(
            "aaa", "bbb", datetime.datetime(2020, 12, 2, 15, 4), ("foo", "bar")
        )

        # Act (actually perform what has to be done)
        # Assert (verify the results)
        self.assertFalse(entry_1 < entry_2)
        self.assertLess(entry_2, entry_1)
        self.assertLessEqual(entry_2, entry_1)

    def test_lt_category(self):
        # Arrange (set up test environment)
        entry_1 = CalenderEntry(
            "aaa", "zzz", datetime.datetime(2021, 12, 2, 15, 4), ("foo", "bar")
        )
        entry_2 = CalenderEntry(
            "aaa", "bbb", datetime.datetime(2021, 12, 2, 15, 4), ("foo", "bar")
        )

        # Act (actually perform what has to be done)
        # Assert (verify the results)
        self.assertFalse(entry_1 < entry_2)
        self.assertLess(entry_2, entry_1)
        self.assertLessEqual(entry_2, entry_1)

    def test_lt_title(self):
        # Arrange (set up test environment)
        entry_1 = CalenderEntry(
            "zzz", "bbb", datetime.datetime(2021, 12, 2, 15, 4), ("foo", "bar")
        )
        entry_2 = CalenderEntry(
            "aaa", "bbb", datetime.datetime(2021, 12, 2, 15, 4), ("foo", "bar")
        )

        # Act (actually perform what has to be done)
        # Assert (verify the results)
        self.assertFalse(entry_1 < entry_2)
        self.assertLess(entry_2, entry_1)
        self.assertLessEqual(entry_2, entry_1)


@tag("interfaces", "data", "calenderentrylist")
class CalenderEntryListTest(CalingenTestCase):
    """Provide tests for the CalenderEntryList class."""

    def test_constructor_initializes_set(self):
        """Constructor initializes _entries."""
        # Arrange (set up test environment)
        cal_entry_list = CalenderEntryList()

        # Act (actually perform what has to be done)

        # Assert (verify the results)
        self.assertIsInstance(cal_entry_list._entries, set)

    def test_add_adds_provided_entry(self):
        """add() appends provided entry to _entries."""
        # Arrange (set up test environment)
        cal_entry_list = CalenderEntryList()
        test_entry = "foo"

        # Act (actually perform what has to be done)
        cal_entry_list.add(test_entry)

        # Assert (verify the results)
        self.assertIn(test_entry, cal_entry_list._entries)

    def test_add_rejects_none(self):
        """add() rejects if parameter is None."""
        # Arrange (set up test environment)
        cal_entry_list = CalenderEntryList()

        # Act (actually perform what has to be done)
        # Assert (verify the results)
        with self.assertRaises(CalenderEntryList.CalenderEntryListException):
            cal_entry_list.add(None)

    def test_merge_merges_distinct_sets(self):
        """merge() correctly merges two distinct CalenderEntryList instances."""
        # Arrange (set up test environment)
        cal_entry_one = CalenderEntry(
            title="foo",
            category="foo",
            timestamp=datetime.datetime.now(),
            source=("foo", "bar"),
        )
        cal_entry_two = CalenderEntry(
            title="bar",
            category="bar",
            timestamp=datetime.datetime.now(),
            source=("foo", "bar"),
        )

        cal_entry_list_target = CalenderEntryList()
        cal_entry_list_target.add(cal_entry_one)

        cal_entry_list_second = CalenderEntryList()
        cal_entry_list_second.add(cal_entry_two)

        # Act (actually perform what has to be done)
        cal_entry_list_target.merge(cal_entry_list_second)

        # Assert (verify the results)
        self.assertIn(cal_entry_one, cal_entry_list_target._entries)
        self.assertIn(cal_entry_two, cal_entry_list_target._entries)

    def test_merge_merges_non_distinct_sets(self):
        """merge() correctly merges two non distinct CalenderEntryList instances."""
        # Arrange (set up test environment)
        cal_entry_one = CalenderEntry(
            title="foo",
            category="foo",
            timestamp=datetime.datetime.now(),
            source=("foo", "bar"),
        )
        cal_entry_two = CalenderEntry(
            title="bar",
            category="bar",
            timestamp=datetime.datetime.now(),
            source=("foo", "bar"),
        )

        cal_entry_list_target = CalenderEntryList()
        cal_entry_list_target.add(cal_entry_one)

        cal_entry_list_second = CalenderEntryList()
        cal_entry_list_second.add(cal_entry_two)
        cal_entry_list_second.add(cal_entry_one)

        # Act (actually perform what has to be done)
        cal_entry_list_target.merge(cal_entry_list_second)

        # Assert (verify the results)
        self.assertIn(cal_entry_one, cal_entry_list_target._entries)
        self.assertIn(cal_entry_two, cal_entry_list_target._entries)
        self.assertEqual(len(cal_entry_list_target._entries), 2)
