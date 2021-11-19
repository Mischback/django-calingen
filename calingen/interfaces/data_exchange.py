# SPDX-License-Identifier: MIT

"""Provides data exchange formats."""

# Python imports
from collections import namedtuple

CalenderEntry = namedtuple("CalenderEntry", "title category start")
"""This data structure is used to pass calender entries around.

Warnings
--------
This data structure does not provide any validation of its values / fields.

Following EAFP: the consuming code **must ensure** that the received data is of
the expected type.

Notes
-----
The structure contains an entries ``title``, ``category`` and its ``start`` date and
time (as :py:obj:`datetime.datetime`).

This is implemented as :py:obj:`collections.namedtuple`.
"""


class CalenderEntryList(object):
    """A list of calender entries."""

    _entries = []

    def add_entry(self, entry, title=None, category=None, start=None):
        """Just for linting."""
        if entry is None:
            if (title is None) or (category is None) or (start is None):
                raise Exception("Could not add entry!")

            entry = CalenderEntry(title, category, start)

        self._entries.append(entry)

    def merge(self, entry_list_instance):
        """Just for linting."""
        self._entries += entry_list_instance._entries
