# SPDX-License-Identifier: MIT

"""Provide the app's user profile."""

# Python imports
import logging

# Django imports
from django import forms
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

# app imports
from calingen.forms.fields.plugin import PluginField
from calingen.interfaces.plugin_api import EventProvider
from calingen.models.queryset import CalingenQuerySet

logger = logging.getLogger(__name__)


class ProfileQuerySet(CalingenQuerySet):  # noqa: D101
    pass


class ProfileManager(models.Manager):
    """Just for linting, will be refactored!"""  # noqa: D400

    def get_queryset(self):
        """Just for linting, will be refactored!"""  # noqa: D400
        return ProfileQuerySet(self.model, using=self._db).default()


class Profile(models.Model):
    """Represents the app-specific profile.

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

    calingen_manager = ProfileManager()
    """App-/model-specific manager, that provides additional functionality.

    This manager is set to
    :class:`calingen.models.profile.ProfileManager`. Its implementation provides
    augmentations of `Profile` objects, by annotating them on database level.
    This will reduce the number of required database queries, if attributes of
    the object are accessed.

    The manager has to be used explicitly.
    """

    _event_provider = models.JSONField(
        default=dict, blank=True, verbose_name=_("Event Provider")
    )
    """List of activated :class:`~calingen.interfaces.plugin_api.EventProvider` plugins.

    Notes
    -----
    This is implemented as a :class:`~django.db.models.JSONField`.
    """

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Owner")
    )
    """Reference to a Django `User`.

    Notes
    -----
    This is implemented as a :class:`~django.db.models.OneToOneField` with
    ``on_delete=CASCADE``, meaning: if the referenced `User` object is deleted,
    the referencing `Profile` object is discarded aswell.

    To keep this application as pluggable as possible, the referenced class is
    dependent on :setting:`AUTH_USER_MODEL`. With this implementation, the
    project may substitute the :class:`~django.contrib.auth.models.User` model
    provided by Django without breaking any functionality in `calingen` (see
    :djangodoc:`Reusable Apps and AUTH_USER_MODEL <topics/auth/customizing/#reusable-apps-and-auth-user-model>`).
    """

    class Meta:  # noqa: D106
        app_label = "calingen"
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):  # noqa: D105
        return "[Profile] {}".format(self.owner)  # pragma: nocover

    def get_absolute_url(self):
        """Return the absolute URL for instances of this model.

        Returns
        -------
        str
            The absolute URL for instances of this model.
        """
        return reverse("profile-update", args=[self.id])  # pragma: nocover

    @property
    def event_provider(self):  # noqa: D102
        raw = self._event_provider

        provider = [p[0] for p in EventProvider.list_available_plugins()]

        active = []
        unavailable = []

        for item in raw.get("active", []):
            if item in provider:
                active.append(item)
            else:
                unavailable.append(item)

        for item in raw.get("unavailable", []):
            if item in provider:
                active.append(item)
            else:
                unavailable.append(item)

        result = {}
        result["active"] = active
        result["unavailable"] = unavailable

        logger.debug(result)
        return result

    @event_provider.setter
    def event_provider(self, value):
        self._event_provider = value
        self.save()


class ProfileForm(forms.ModelForm):
    """Used to validate input for creating and updating :class:`~calingen.models.profile.Profile` instances."""

    event_provider = PluginField(
        required=False, choices=EventProvider.list_available_plugins
    )

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance", None)
        if instance is not None:
            kwargs["initial"] = {"event_provider": instance.event_provider}
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):  # noqa: D102
        self.instance.event_provider = self.cleaned_data["event_provider"]
        return super().save(*args, **kwargs)

    class Meta:  # noqa: D106
        model = Profile
        fields = ["event_provider"]
