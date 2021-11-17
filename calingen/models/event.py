# SPDX-License-Identifier: MIT

"""Provide the app's central class to store and manage calender entries."""

# Django imports
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Event(models.Model):
    """Represents one event in a user's calender.

    Warnings
    --------
    The class documentation only includes code that is actually shipped by the
    `calingen` app. Inherited attributes/methods (provided by Django's
    :class:`~django.db.models.Model`) are not documented here.
    """

    class EventType(models.TextChoices):
        """Provides the accepted choices for :attr:`calingen.models.event.Event.type`."""

        ANNUAL_ANNIVERSARY = "ANNUAL_ANNIVERSARY", _("Annual Anniversary")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("Owner"),
    )
    """Reference to a Django `User`.

    Notes
    -----
    This is implemented as a :class:`~django.db.models.ForeignKey` with
    ``on_delete=CASCADE``, meaning: if the referenced `User` object is deleted,
    all referencing `Event` objects are discarded aswell.

    The backwards relation (see
    :attr:`ForeignKey.related_name<django.db.models.ForeignKey.related_name>`) is
    disabled.

    To keep this application as pluggable as possible, the referenced class is
    dependent on :setting:`AUTH_USER_MODEL`. With this implementation, the
    project may substitute the :class:`~django.contrib.auth.models.User` model
    provided by Django without breaking any functionality in `calingen` (see
    :djangodoc:`Reusable Apps and AUTH_USER_MODEL <topics/auth/customizing/#reusable-apps-and-auth-user-model>`).
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
    its possible values limited by :class:`calingen.models.event.Event.EventType`.
    """

    class Meta:  # noqa: D106
        app_label = "calingen"
        unique_together = ["title", "start"]
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __str__(self):  # noqa: D105
        return "[{}] [{}] {} - {}".format(
            self.type, self.owner, self.title, self.start
        )  # pragma: nocover
