# SPDX-License-Identifier: MIT

"""Provides data exchange formats."""

# Python imports
import datetime
from functools import total_ordering

# external imports
from dateutil import parser

# app imports
from calingen.constants import EventCategory
from calingen.exceptions import CallingenInterfaceException

SOURCE_INTERNAL = "INTERNAL"
SOURCE_EXTERNAL = "EXTERNAL"


@total_ordering
class CalenderEntry:
    """Data structure to pass calender entries around."""

    class CalenderEntryException(CallingenInterfaceException):
        """Class-specific exception, raised on failures in this class's methods.

        Warnings
        --------
        The instances' ``source`` attribute is not included in checks for
        equality (``__eq__()``) or during hash-processing (``__hash__()``)!

        This means, that if an event is specified by an external provider and
        by using the app's :class:`calingen.models.event.Event` model, using
        the same ``title``, ``category`` and ``timestamp``, they are considered
        **equal**.

        The implementation of
        :class:`calingen.interfaces.data_exchange.CalenderEntryList` relies
        internally on a ``set``, which means the entries are unique. So, only
        one of the events will be present in the resulting ``CalenderEntryList``.
        """

    def __init__(self, title, category, timestamp, source):
        self.title = title

        # Use the (lazy) translatable category (if available)
        if category in EventCategory.values:
            self.category = EventCategory[category].label  # pragma: nocover
        else:
            self.category = category

        # Ensure that "timestamp" is a datetime.datetime object
        if isinstance(timestamp, datetime.datetime):
            self.timestamp = timestamp
        elif isinstance(timestamp, datetime.date):
            self.timestamp = datetime.datetime.combine(timestamp, datetime.time.min)
        else:
            # Delegate parsing to dateutil; probably breaks if unparsable
            # Django uses datetime.datetime.strptime(), dateutil.parser should
            # be "more forgiving". And while we rely on that package anyway...
            self.timestamp = parser.parse(timestamp)

        # "source" is expected to be a tuple of the the form
        # (SOURCE_INTERNAL, Event.id) or (SOURCE_EXTERNAL, EventProvider.title)
        if isinstance(source, tuple):
            self.source = source
        else:
            raise self.CalenderEntryException("source must be provided as tuple")

    def __eq__(self, other):  # noqa: D105
        # see https://stackoverflow.com/a/2909119
        # see https://stackoverflow.com/a/8796908
        if isinstance(other, CalenderEntry):
            return self.__key() == other.__key()  # pragma: nocover
        return NotImplemented

    def __lt__(self, other):  # noqa: D105
        # see https://stackoverflow.com/a/8796908
        if isinstance(other, CalenderEntry):
            return self.__key() < other.__key()
        return NotImplemented

    def __repr__(self):  # noqa: D105
        # see https://stackoverflow.com/a/12448200
        return "<CalenderEntry(title={}, category={}, start={}, source={})>".format(
            self.title.__repr__(),
            self.category.__repr__(),
            self.timestamp.__repr__(),
            self.source.__repr__(),
        )  # pragma: nocover

    def __str__(self):  # noqa: D105
        # see https://stackoverflow.com/a/12448200
        return "[{}] {} ({})".format(
            self.timestamp, self.title, self.category
        )  # pragma: nocover

    def __hash__(self):  # noqa: D105
        # see https://stackoverflow.com/a/2909119
        return hash(self.__key())  # pragma: nocover

    def __key(self):
        # see https://stackoverflow.com/a/2909119
        return (self.timestamp, self.category, self.title)  # pragma: nocover


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
        return len(self._entries)  # pragma: nocover

    def add(self, entry):
        """Add a :class:`~calingen.interfaces.data_exchange.CalenderEntry` to the list.

        Parameters
        ----------
        entry : CalenderEntry
            The entry to be added to this class's list. If set to ``None``, the
            optional parameters are used to create an instance of
            :class:`~calingen.interfaces.data_exchange.CalenderEntry` and add
            that.

        Warnings
        --------
        There is no validation of the input type!
        """
        if entry is None:
            raise self.CalenderEntryListException("An entry is required")

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
        return sorted(self._entries)  # pragma: nocover
