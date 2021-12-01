# SPDX-License-Identifier: MIT

"""Provide the app's central class to store and manage calender entries."""

# Django imports
from django import forms
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

# app imports
from calingen.constants import EventType
from calingen.exceptions import CalingenException
from calingen.forms.fields import SplitDateTimeOptionalField
from calingen.interfaces.data_exchange import CalenderEntryList
from calingen.models.profile import Profile
from calingen.models.queryset import CalingenQuerySet


class EventModelException(CalingenException):
    """Base class for all exceptions related to the :class:`~calingen.models.event.Event` model."""


class EventQuerySet(CalingenQuerySet):
    """App-specific implementation of :class:`django.db.models.QuerySet`.

    Notes
    -----
    This :class:`~django.db.models.QuerySet` implementation provides
    app-specific augmentations.

    The provided methods augment/extend the retrieved
    :class:`calingen.models.event.Event` instances by annotating them with
    additional information.
    """

    def default(self):
        """Return a :class:`~django.db.models.QuerySet` with annotations.

        Returns
        -------
        :class:`~django.db.models.QuerySet`
            The annotated queryset.
        """
        return self

    def filter_by_user(self, user):
        """Filter the result set by the objects' :attr:`owners <calingen.models.profile.Profile.owner>`.

        Parameters
        ----------
        user :
            An instance of the project's user model, as specified by
            :setting:`AUTH_USER_MODEL`.

        Returns
        -------
        :class:`django.db.models.QuerySet`
            The filtered queryset.

        Notes
        -----
        Effectively, this method is used to ensure, that any user may only
        access objects, which are owned by him. This is the app's way of
        ensuring `row-level permissions`, because only owners are allowed to
        view (and modify) their events.
        """
        return self.filter(profile__owner=user)


class EventManager(models.Manager):
    """App-/model-specific implementation of :class:`django.db.models.Manager`.

    Notes
    -----
    This :class:`~django.db.models.Manager` implementation is used as an
    additional manager of :class:`~calingen.models.event.Event` (see
    :attr:`calingen.models.event.Event.calingen_manager`).

    This implementation inherits its functionality from
    :class:`django.db.models.Manager` and provides identical funtionality.
    Furthermore, it augments the retrieved objects with additional attributes,
    using the custom :class:`~django.db.models.QuerySet` implementation
    :class:`~calingen.models.event.EventQuerySet`.
    """

    def get_calender_entry_list(self, user=None):
        """Return all instances as :class:`~calingen.interfaces.data_exchange.CalenderEntryList`.

        Parameters
        ----------
        user :
            The summary is provided for an actual user, filtered by
            :attr:`calingen.models.event.Event.owner`.

            Most likely you will want to pass ``request.user`` into the method.

        Returns
        -------
        :class:`~calingen.interfaces.data_exchange.CalenderEntryList`
            All :class:`~calingen.models.event.Event` instances of ``user``,
            converted into a ``CalenderEntryList``.
        """
        result = CalenderEntryList()
        for event in self.get_user_events_qs(user).iterator():
            result.add_entry(
                None, title=event.title, category=event.type, start=event.start
            )

        return result

    def get_queryset(self):
        """Use the app-/model-specific :class:`~calingen.models.event.EventQuerySet` by default.

        Returns
        -------
        :class:`django.models.db.QuerySet`
            This queryset is provided by
            :class:`calingen.models.event.EventQuerySet` and applies its
            :meth:`~calingen.models.event.EventQuerySet.default` method. The
            retrieved objects will be annotated with additional attributes.
        """
        return EventQuerySet(self.model, using=self._db).default()

    def get_user_events_qs(self, user=None):
        """Provide a ``QuerySet`` containing all events of a given ``user``.

        Parameters
        ----------
        user :
            The summary is provided for an actual user, filtered by
            :attr:`calingen.models.event.Event.owner`.

            Most likely you will want to pass ``request.user`` into the method.

        Returns
        -------
        :class:`django.models.db.QuerySet`
            This queryset is provided by
            :class:`calingen.models.event.EventQuerySet` and applies its
            :meth:`~calingen.models.event.EventQuerySet.filter_by_user` method.
        """
        if user is None:
            raise EventModelException(
                "This method may only be called with a user object"
            )
        return self.get_queryset().filter_by_user(user)

    def summary(self, user=None):
        """Provide a user-specific summary of :class:`~calingen.models.event.Event` instances.

        Parameters
        ----------
        user :
            The summary is provided for an actual user, filtered by
            :attr:`calingen.models.event.Event.owner`.

            Most likely you will want to pass ``request.user`` into the method.

        Returns
        -------
        int
            As of now, the method only returns the number of instances.
        """
        return self.get_user_events_qs(user).count()


class Event(models.Model):
    """Represents one event in a user's calender.

    Warnings
    --------
    The class documentation only includes code that is actually shipped by the
    `calingen` app. Inherited attributes/methods (provided by Django's
    :class:`~django.db.models.Model`) are not documented here.
    """

    objects = models.Manager()
    """The model's default manager.

    The default manager is set to :class:`django.db.models.Manager`, which is
    the default value. In order to add the custom :attr:`calingen_manager` as
    an *additional* manager, the default manager has to be provided explicitly
    (see :djangodoc:`topics/db/managers/#default-managers`).
    """

    calingen_manager = EventManager()
    """App-/model-specific manager, that provides additional functionality.

    This manager is set to
    :class:`calingen.models.event.EventManager`. Its implementation provides
    augmentations of `Event` objects, by annotating them on database level.
    This will reduce the number of required database queries, if attributes of
    the object are accessed.

    The manager has to be used explicitly.
    """

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="events",
        verbose_name=Profile._meta.verbose_name,
    )
    """Reference to a :class:`~calingen.models.profile.Profile` object.

    Notes
    -----
    This is implemented as a :class:`~django.db.models.ForeignKey` with
    ``on_delete=CASCADE``, meaning: if the referenced
    :class:`~calingen.models.profile.Profile` object is deleted,
    all referencing ``Event`` objects are discarded aswell.

    The backwards relation (see
    :attr:`ForeignKey.related_name<django.db.models.ForeignKey.related_name>`)
    is named ``"events"``.
    """

    start = models.DateTimeField(
        help_text=_("The start date and time for this recurring event."),
        verbose_name=_("Start Date"),
    )
    """Date and time of a recurring event (:py:obj:`datetime.datetime`).

    Warnings
    --------
    The name of this attribute might be misleading at first. `calingen` will be
    developed in small steps, of which the first one will be to track annual
    aniversaries with the `Event` class. Nevertheless, it is planned to enable
    `calingen` to track generic recurring events. In that implementation step,
    `Event` instances will have a start and end ``datetime``.

    To ease the refactoring, this attribute is already named **start**.

    Notes
    -----
    The attribute is implemented as :class:`~django.db.models.DateTimeField`.
    """

    title = models.CharField(
        max_length=50,
        help_text=_(
            "This will be included in the generated output and is capped at 50 characters."
        ),
        verbose_name=_("Event Title"),
    )
    """The actual title of this `Event` (:py:obj:`str`).

    Notes
    -----
    The attribute is implemented as :class:`~django.db.models.CharField`.
    """

    type = models.CharField(
        max_length=18,
        choices=EventType.choices,
        default=EventType.ANNUAL_ANNIVERSARY,
        help_text=_("The type of this event."),
        verbose_name=_("Event Type"),
    )
    """The type of this `Event`.

    Notes
    -----
    Some functionalities of the `Event` class depend on the actual `EventType`
    stored in this attribute.

    The attribute is implemented as :class:`~django.db.models.CharField` with
    its possible values limited by :class:`calingen.constants.EventType`.
    """

    class Meta:  # noqa: D106
        app_label = "calingen"
        unique_together = ["title", "start"]
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __str__(self):  # noqa: D105
        return "[{}] [{}] {} - {}".format(
            self.type, self.profile, self.title, self.start
        )  # pragma: nocover

    def get_absolute_url(self):
        """Return the absolute URL for instances of this model.

        Returns
        -------
        str
            The absolute URL for instances of this model.
        """
        return reverse("event-detail", args=[self.id])  # pragma: nocover


class EventForm(forms.ModelForm):
    """Used to validate input for creating and updating `Event` instances."""

    start = SplitDateTimeOptionalField()

    class Meta:  # noqa: D106
        model = Event
        fields = ["type", "title", "start"]
