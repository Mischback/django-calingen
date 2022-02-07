# SPDX-License-Identifier: MIT

"""App-specific user profile.

Beside the actual :class:`calingen.models.profile.Profile` model, this module
contains the related implementations of :class:`django.db.models.QuerySet`,
:class:`django.db.models.Manager` and :class:`django.forms.ModelForm`.
"""

# Python imports
import datetime

# Django imports
from django import forms
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

# app imports
from calingen.forms.fields import PluginField
from calingen.interfaces.data_exchange import CalendarEntryList
from calingen.interfaces.plugin_api import EventProvider
from calingen.models.queryset import CalingenQuerySet


class ProfileQuerySet(CalingenQuerySet):
    """App-specific implementation of :class:`django.db.models.QuerySet`.

    Notes
    -----
    This :class:`~django.db.models.QuerySet` implementation provides
    app-specific augmentations.

    The provided methods augment/extend the retrieved
    :class:`calingen.models.profile.Profile` instances by annotating them with
    additional information.
    """

    def default(self):
        """Return a :class:`~django.db.models.QuerySet` with annotations.

        Returns
        -------
        :class:`~django.db.models.QuerySet`
            The annotated queryset.

        Notes
        -----
        The following annotations are provided by default:

        - :meth:`~calingen.models.profile.ProfileQuerySet._owner`
        - :meth:`~calingen.models.profile.ProfileQuerySet._event_count`
        """
        return self._owner()._event_count()

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
        return self.filter(owner=user)

    def _event_count(self):
        """Annotate each instance with the count of associated :class:`~calingen.models.event.Event` instances.

        Returns
        -------
        :class:`~django.db.models.QuerySet`
            The annotated queryset. The annotation will be available as
            ``event_count``.

        Notes
        -----
        This annotation is provided in
        :meth:`~calingen.models.profile.ProfileQuerySet.default`.
        """
        return self.annotate(event_count=models.Count("events"))

    def _owner(self):
        """Make :attr:`Profile.owner <calingen.models.profile.Profile.owner>` available.

        Returns
        -------
        :class:`~django.db.models.QuerySet`
            Instances of :class:`~calingen.models.profile.Profile` will have
            their :attr:`~calingen.models.profile.Profile.owner` available
            without another database query.

        Notes
        -----
        This method makes the associated project user (specified by
        :setting:`AUTH_USER_MODEL` and stored in
        :attr:`Profile.owner <calingen.models.profile.Profile.owner>`) available.

        This annotation is provided in
        :meth:`~calingen.models.profile.ProfileQuerySet.default`.
        """
        return self.select_related("owner")  # pragma: nocover


class ProfileManager(models.Manager):
    """App-/model-specific implementation of :class:`django.db.models.Manager`.

    Notes
    -----
    This :class:`~django.db.models.Manager` implementation is used as an
    **additional** manager of :class:`~calingen.models.profile.Profile`
    (see :attr:`calingen.models.profile.Profile.calingen_manager`).

    This implementation inherits its functionality from
    :class:`django.db.models.Manager` and provides identical funtionality.
    Furthermore, it augments the retrieved objects with additional attributes,
    using the custom :class:`~django.db.models.QuerySet` implementation
    :class:`~calingen.models.profile.ProfileQuerySet`.
    """

    def get_queryset(self):
        """Use the app-/model-specific :class:`~calingen.models.profile.ProfileQuerySet` by default.

        Returns
        -------
        :class:`django.models.db.QuerySet`
            This queryset is provided by
            :class:`calingen.models.profile.ProfileQuerySet` and applies its
            :meth:`~stockings.models.profile.ProfileQuerySet.default`
            method. The retrieved objects will be annotated with additional
            attributes.
        """
        return ProfileQuerySet(self.model, using=self._db).default()  # pragma: nocover

    def get_profile(self, user):
        """Retrieve the :class:`~calingen.models.profile.Profile` associated with a ``User`` instance.

        Parameters
        ----------
        user :
            An instance of the project's user model, as specified by
            :setting:`AUTH_USER_MODEL`.

        Returns
        -------
        :class:`calingen.models.profile.Profile`
            The ``Profile`` associated with the given ``user``.
        """
        try:
            return self.get(owner=user)
        except self.model.DoesNotExist:
            return None


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
    """Manage :class:`~calingen.interfaces.plugin_api.EventProvider` plugins for this profile.

    Notes
    -----
    This is implemented as a :class:`~django.db.models.JSONField` and should be
    interfaced by its custom
    :meth:`~calingen.models.profile.Profile.event_provider` getter and setter
    methods, provided as a ``property``.
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
        return reverse("calingen:profile", args=[self.id])  # pragma: nocover

    def resolve(self, year=None):
        """Combine all event providers results for a given year into one :class:`~calingen.interfaces.data_exchange.CalendarEntryList`.

        Parameters
        ----------
        year : int, optional
            The year to use for resolving the
            :class:`~calingen.interfaces.plugin_api.EventProvider`.

        Returns
        -------
        :class:`~calingen.interfaces.data_exchange.CalendarEntryList`
            A single instance including all events from all active providers.
        """
        if year is None:
            year = datetime.datetime.now().year

        result = CalendarEntryList()
        for provider in self.event_provider["active"]:
            provider_instance = import_string(provider)
            result.merge(provider_instance.resolve(year))

        return result

    @property
    def event_provider(self):
        """Get and set the list of :class:`~calingen.interfaces.plugin_api.EventProvider`.

        This method is used to access the ``Profile``'s ``EventProvider``. The
        returned object will have three attributes, ``active``, ``unavailable``
        and ``newly_unavailable``: ``active`` contains the selected ``EventProvider``
        plugins, **that are currently active in this project**. If the user
        had selected ``EventProvider`` plugins, that are currently not available
        in this project, i.e. because they were deactivated by the administrator,
        these plugins are moved to ``unavailable``. Also, these plugins are
        included in ``newly_unavailable`` and then picked up in the
        :meth:`~calingen.views.profile.ProfileUpdateView.get_context_data`
        method to provide messages to the user.

        Notes
        -----
        While the implementation of the ``getter`` involves some logic to
        perform the operations as described above, the ``setter`` simply applies
        the provided value to
        :attr:`~calingen.models.profule.Profile._event_provider`. This means,
        that if the user did not actually **update** its profile, the operation
        performed by the ``getter`` is simply discarded.
        """
        raw = self._event_provider

        provider = [p[0] for p in EventProvider.list_available_plugins()]

        active = []
        unavailable = []
        newly_unavailable = []

        for item in raw.get("active", []):
            if item in provider:
                active.append(item)
            else:
                newly_unavailable.append(item)
                unavailable.append(item)

        for item in raw.get("unavailable", []):
            if item in provider:
                active.append(item)
            else:
                unavailable.append(item)

        result = {}
        result["active"] = active
        result["unavailable"] = unavailable
        result["newly_unavailable"] = newly_unavailable

        return result

    @event_provider.setter
    def event_provider(self, value):  # pragma: nocover
        if value is None:
            value = dict()
        self._event_provider = value
        self.save()


class ProfileForm(forms.ModelForm):
    """Used to validate input for creating and updating :class:`~calingen.models.profile.Profile` instances."""

    event_provider = PluginField(
        required=False, choices=EventProvider.list_available_plugins
    )
    """Manually add the model's ``property`` to the form.

    Notes
    -----
    :class:`~django.forms.ModelForm` only includes actual model fields.
    :attr:`calingen.models.profile.Profile.event_provider` is actually only a
    ``property`` to interface
    :attr:`~calingen.models.profile.Profile._event_provider`.

    The ``property`` is added here and then applied in the form's
    :meth:`~calingen.models.profile.ProfileForm.save` method.
    """

    def __init__(self, *args, **kwargs):  # pragma: nocover
        instance = kwargs.get("instance", None)
        if instance is not None:
            kwargs["initial"] = {"event_provider": instance.event_provider}
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):  # pragma: nocover
        """Inject the value of ``event_provider`` into the instance and save it."""
        self.instance.event_provider = self.cleaned_data["event_provider"]
        return super().save(*args, **kwargs)

    class Meta:  # noqa: D106
        model = Profile
        fields = ["event_provider"]
