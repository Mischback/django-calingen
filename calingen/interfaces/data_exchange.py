# SPDX-License-Identifier: MIT

"""Provides data exchange formats."""

# Python imports
from functools import total_ordering

# app imports
from calingen.exceptions import CallingenInterfaceException


@total_ordering
class CalenderEntry:
    """Data structure to pass calender entries around."""

    def __init__(self, title, category, timestamp):
        self.title = title
        self.category = category
        self.timestamp = timestamp

    def __eq__(self, other):  # noqa: D105
        # see https://stackoverflow.com/a/2909119
        # see https://stackoverflow.com/a/8796908
        if isinstance(other, CalenderEntry):
            return self.__key() == other.__key()
        return NotImplemented

    def __lt__(self, other):  # noqa: D105
        # see https://stackoverflow.com/a/8796908
        if isinstance(other, CalenderEntry):
            return self.__key() < other.__key()
        return NotImplemented

    def __repr__(self):  # noqa: D105
        # see https://stackoverflow.com/a/12448200
        return "<CalenderEntry(title={}, category={}, start={})>".format(
            self.title.__repr__(), self.category.__repr__(), self.timestamp.__repr__()
        )

    def __str__(self):  # noqa: D105
        # see https://stackoverflow.com/a/12448200
        return "[{}] {} ({})".format(self.timestamp, self.title, self.category)

    def __hash__(self):  # noqa: D105
        # see https://stackoverflow.com/a/2909119
        return hash(self.__key())

    def __key(self):
        # see https://stackoverflow.com/a/2909119
        return (self.timestamp, self.category, self.title)


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

    def add_entry(self, entry, title=None, category=None, timestamp=None):
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
            # FIXME: This is not longer required, if the refactoring of CalenderEntry works!
            if (title is None) or (category is None) or (timestamp is None):
                raise self.CalenderEntryListException("Could not add entry!")

            entry = CalenderEntry(title, category, timestamp)

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
        return sorted(self._entries, key=lambda entry: entry.timestamp)
