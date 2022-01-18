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
"""Constant for app-internal :class:`~calingen.models.event.Event` instances."""

SOURCE_EXTERNAL = "EXTERNAL"
"""Constant for entries provided by implementations of :class:`calingen.interfaces.plugin_api.EventProvider`"""


@total_ordering
class CalendarEntry:
    """Data structure to pass calendar entries around.

    Parameters
    ----------
    title : str
    category : calingen.constants.EventCategory.value
    timestamp : datetime.datetime, datetime.date, str
    source : tuple

    Attributes
    ----------
    title : str
        The actual title of the entry.
    category : str
        While this is actually a simple :py:obj:`str`, it is expected to be of
        the specified type. A lookup against
        :attr:`EventCategory.values <calingen.constants.EventCategory.values>`
        is performed, but this is not an enforced validation!

        If the ``constructor`` was called with an instance of
        :attr:`EventCategory.value <calingen.constants.EventCategory.value>`,
        this will be a `translateable` string.
    timestamp : datetime.datetime
        The paremeter accepts the specified types and will convert them to
        :py:obj:`datetime.datetime` internally.
        If a :py:obj:`str` is given, :meth:`dateutil.parser.parse` is used and
        may raise an exception, if the provided string could not be parsed.
    source : tuple
        Expected is a tuple of the form ``("INTERNAL", [int])``, where ``[int]``
        is interpreted as an ``id`` of an :class:`~calingen.models.event.Event`
        instance, or ``("EXTERNAL", [str])``, where ``[str]`` is used as a plain
        string.

        For implementations of
        :class:`~calingen.interfaces.plugin_api.EventProvider` it is recommended
        to provide its ``title`` attribute.

    Raises
    ------
    CalendarEntry.CalendarEntryException
        Raised if ``source`` was not provided as :py:obj:`tuple`
    dateutil.parser._parser.ParserError
        Raised if ``timestamp`` is provided as :py:obj:`str` and could not be
        parsed by :meth:`dateutil.parser.parse`

    Warnings
    --------
    The instance's ``source`` attribute is not included in checks for
    equality (``__eq__()``) or during hash-processing (``__hash__()``)!

    This means, that if an event is specified by an external provider and
    by using the app's :class:`calingen.models.event.Event` model, using
    the same ``title``, ``category`` and ``timestamp``, they are considered
    **equal**.

    The implementation of
    :class:`calingen.interfaces.data_exchange.CalendarEntryList` relies
    internally on a ``set``, which means the entries are unique. So, only
    one of the events will be present in the resulting ``CalendarEntryList``.

    Notes
    -----
    Instances of this class are single, self-contained entries in a calendar.
    They provide an abstraction and common interface to events provided by the
    app's user (instances of :class:`~calingen.models.event.Event`) and events
    provided by plugins (implementations of
    :class:`~calingen.interfaces.plugin_api.EventProvider`).

    However, there is no real case of using this class without and accompanying
    :class:`~calingen.interfaces.data_exchange.CalendarEntryList`. Actually,
    all ``resolve()`` operations are required to return an instance of
    :class:`~calingen.interfaces.data_exchange.CalendarEntryList` with instances
    of this class as its payload.

    As you can see, the documentation of the class's `magic methods` is kept at
    a minimum. See the source code for further details!
    """

    class CalendarEntryException(CallingenInterfaceException):
        """Class-specific exception, raised on failures in this class's methods."""

    def __init__(self, title, category, timestamp, source):
        # documentation of the costructor is in the class's docstring!
        self.title = title

        # Use the predefined category (if available)
        if category in EventCategory.values:
            self.category = EventCategory[category]
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
            raise self.CalendarEntryException("source must be provided as tuple")

    def __eq__(self, other):
        """Check equality with ``other`` object."""
        # see https://stackoverflow.com/a/2909119
        # see https://stackoverflow.com/a/8796908
        if isinstance(other, CalendarEntry):
            return self.__key() == other.__key()  # pragma: nocover
        return NotImplemented

    def __lt__(self, other):
        """Provide `less than` comparison with ``other`` object."""
        # see https://stackoverflow.com/a/8796908
        if isinstance(other, CalendarEntry):
            return self.__key() < other.__key()
        return NotImplemented

    def __repr__(self):
        """Provide an instance's `representation`."""
        # see https://stackoverflow.com/a/12448200
        return "<CalendarEntry(title={}, category={}, start={}, source={})>".format(
            self.title.__repr__(),
            self.category.__repr__(),
            self.timestamp.__repr__(),
            self.source.__repr__(),
        )  # pragma: nocover

    def __str__(self):
        """Provide a string representation of the instance."""
        # see https://stackoverflow.com/a/12448200
        return "[{}] {} ({})".format(
            self.timestamp, self.title, self.category
        )  # pragma: nocover

    def __hash__(self):
        """Provide a unique representation of the instance."""
        # see https://stackoverflow.com/a/2909119
        return hash(self.__key())  # pragma: nocover

    def __key(self):
        """Provide internal representation of the instance."""
        # see https://stackoverflow.com/a/2909119
        return (self.timestamp, self.category, self.title)  # pragma: nocover


class CalendarEntryList:
    """A list of calendar entries.

    Attributes
    ----------
    _entries : set
        This attribute stores the list of calendar entries. It is implemented
        as a :py:obj:`set`, which makes it mutable and unordered. Primarily a
        :py:obj:`set` is used to ensure that all included items are **unique**.

    Warnings
    --------
    While objects of this class are intended to store / handle instances of
    :class:`~calingen.interfaces.data_exchange.CalendarEntry`, this is **not**
    enforced or validated (EAFP).

    Notes
    -----
    This class is a close companion of
    :class:`~calingen.interfaces.data_exchange.CalendarEntry` instances.

    Internally, the app expects the result of any ``resolve()`` operation to be
    an instance of this class with a set (or list) of
    :class:`~calingen.interfaces.data_exchange.CalendarEntry` instances.
    """

    class CalendarEntryListException(CallingenInterfaceException):
        """Class-specific exception, raised on failures in this class's methods."""

    def __init__(self):  # noqa: D107
        self._entries = set()

    def __len__(self):  # noqa: D105
        return len(self._entries)  # pragma: nocover

    def add(self, entry):
        """Add a :class:`~calingen.interfaces.data_exchange.CalendarEntry` to the list.

        Parameters
        ----------
        entry : CalendarEntry
            The entry to be added to this class's list.

        Raises
        ------
        CalendarEntryList.CalendarEntryListException
            Raised if no entry is provided.

        Warnings
        --------
        There is no validation of the input type!
        """
        if entry is None:
            raise self.CalendarEntryListException("An entry is required")

        self._entries.add(entry)

    def merge(self, entry_list_instance):
        """Merge two instances of ``CalendarEntryList``.

        Parameters
        ----------
        entry_list_instance : CalendarEntryList
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
            :class:`~calingen.interfaces.data_exchange.CalendarEntry`.

        Warnings
        --------
        While this class uses internally a ``set`` to manage the entries, this
        method returns a list.

        If consuming code requires uniqueness of items, use this method as late
        as possible.
        """
        return sorted(self._entries)  # pragma: nocover
