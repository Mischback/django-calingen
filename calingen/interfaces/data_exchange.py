# SPDX-License-Identifier: MIT

"""Provides data exchange formats."""

# Python imports
from collections import namedtuple

# app imports
from calingen.exceptions import CallingenInterfaceException

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


class CalenderEntryList:
    """A list of calender entries.

    Attributes
    ----------
    _entries : set
        This attribute stores the list of calender entries. It is implemented
        as a :py:obj:`set`, which makes it mutable and unordered. Primarily a
        :py:obj:`set` is used to ensure that all included items are **unique**.

    Warnings
    --------
    While objects of this class are intended to store / handle instances of
    :class:`~calingen.interfaces.data_exchange.CalenderEntry`, this is **not**
    enforced or validated (EAFP).
    """

    class CalenderEntryListException(CallingenInterfaceException):
        """Class-specific exception, raised on failures in this class's methods."""

    def __init__(self):  # noqa: D107
        self._entries = set()

    def __len__(self):  # noqa: D105
        return len(self._entries)

    def add_entry(self, entry, title=None, category=None, start=None):
        """Add a :class:`~calingen.interfaces.data_exchange.CalenderEntry` to the list.

        Parameters
        ----------
        entry : CalenderEntry
            The entry to be added to this class's list. If set to ``None``, the
            optional parameters are used to create an instance of
            :class:`~calingen.interfaces.data_exchange.CalenderEntry` and add
            that.
        title: str, optional
        category: str, optional
        start: datetime.datetime, optional

        Raises
        ------
        CalenderEntryListException
            If ``entry`` is set to ``None``, ``title``, ``category`` and ``start``
            are expected to be non ``None`` values (see above for the expected,
            but not enforced types). Otherwise, the exception is raised.

        Warnings
        --------
        There is no validation of the input types!
        """
        if entry is None:
            if (title is None) or (category is None) or (start is None):
                raise self.CalenderEntryListException("Could not add entry!")

            entry = CalenderEntry(title, category, start)

        self._entries.add(entry)

    def merge(self, entry_list_instance):
        """Merge two instances of ``CalenderEntryList``.

        Parameters
        ----------
        entry_list_instance : CalenderEntryList
            The instance to be merged into this one.

        Warnings
        --------
        There is no validation of the input type!

        Notes
        -----
        Providing a ``merge()`` method instead of enabling addition of objects
        of this type is a design choice and may be subject to change.
        """
        self._entries.update(entry_list_instance._entries)

    def sorted(self):
        """Return the object's ``_entries`` sorted by ``start``.

        Returns
        -------
        list
            The sorted list of
            :class:`~calingen.interfaces.data_exchange.CalenderEntry`.

        Warnings
        --------
        While this class uses internally a ``set`` to manage the entries, this
        method returns a list.

        If consuming code requires uniqueness of items, use this method as late
        as possible.
        """
        return sorted(self._entries, key=lambda entry: entry.start)
