# SPDX-License-Identifier: MIT

"""Provides data exchange formats."""

# Python imports
from collections import namedtuple

CalenderEntry = namedtuple("CalenderEntry", "title type start")
"""This data structure is used to pass calender entries around.

Warnings
--------
This data structure does not provide any validation of its values / fields.

Following EAFP: the consuming code **must ensure** that the received data is of
the expected type.

Notes
-----
The structure contains an entries ``title``, ``type`` and its ``start`` date and
time (as :py:obj:`datetime.datetime`).

This is implemented as :py:obj:`collections.namedtuple`.
"""


class CalenderEntryList(object):
    """A list of calender entries."""

    def add_entry(self, entry, title=None, type=None, start=None):
        """Just for linting."""
        if entry is None:
            if (title is None) or (type is None) or (start is None):
                # TODO: Provide custom exception class!
                raise Exception("Could not add entry!")

            entry = CalenderEntry(title, type, start)

        # TODO: Add entry to internal list IF NOT ALREADY present

    def merge(self, entry_list_instance):
        """Just for linting."""
        raise NotImplementedError("This is not yet implemented!")
