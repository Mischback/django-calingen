# SPDX-License-Identifier: MIT

"""Provide tests for calingen.interfaces.data_exchange."""

# Python imports
from unittest import mock, skip  # noqa: F401

# Django imports
from django.test import override_settings, tag  # noqa: F401

# app imports
from calingen.interfaces.data_exchange import CalenderEntry, CalenderEntryList

# local imports
from ..util.testcases import CalingenTestCase


@tag("interfaces", "data", "calenderentry")
class CalenderEntryListTest(CalingenTestCase):
    """Provide tests for the CalenderEntryList class."""

    def test_constructor_initializes_set(self):
        """Constructor initializes _entries."""
        # Arrange (set up test environment)
        cal_entry_list = CalenderEntryList()

        # Act (actually perform what has to be done)

        # Assert (verify the results)
        self.assertIsInstance(cal_entry_list._entries, set)

    def test_add_entry_adds_provided_entry(self):
        """add_entry() appends provided entry to _entries."""
        # Arrange (set up test environment)
        cal_entry_list = CalenderEntryList()
        test_entry = "foo"

        # Act (actually perform what has to be done)
        cal_entry_list.add_entry(test_entry)

        # Assert (verify the results)
        self.assertIn(test_entry, cal_entry_list._entries)

    def test_add_entry_adds_constructed_entry(self):
        """add_entry() appends an entry specified by its values to _entries."""
        # Arrange (set up test environment)
        cal_entry_list = CalenderEntryList()
        test_title = "foo"
        test_category = "bar"
        test_start = "baz"

        # Act (actually perform what has to be done)
        cal_entry_list.add_entry(
            None, title=test_title, category=test_category, start=test_start
        )

        # Assert (verify the results)
        self.assertIn(
            CalenderEntry(test_title, test_category, test_start),
            cal_entry_list._entries,
        )

    def test_add_entry_enforces_required_values(self):
        """add_entry() expects an entry or the values to create one."""
        # Arrange (set up test environment)
        cal_entry_list = CalenderEntryList()

        # Assert (verify the results)
        with self.assertRaises(CalenderEntryList.CalenderEntryListException):
            # Act (actually perform what has to be done)
            cal_entry_list.add_entry(None)
