# SPDX-License-Identifier: MIT

"""App-specific mixins to be used with class-based views."""

# Django imports
from django.core.exceptions import ImproperlyConfigured

# app imports
from calingen.interfaces.data_exchange import CalendarEntryList
from calingen.models.event import Event
from calingen.models.profile import Profile


class RestrictToUserMixin:
    """Limits the resulting queryset to objects, that belong to the current user.

    This mixin overwrites the view's ``get_queryset()`` method and automatically
    uses the model's app-specific ``calingen_manager`` with its
    ``filter_by_user()`` method.

    The view, that uses this mixin, must provide the attribute ``model`` to
    actually make this mixin usable by any class-based view of the app.
    """

    def get_queryset(self):
        """Return a queryset that only contains objects, that belong to the current user.

        Internally, the returned queryset will use the app- and model-specific
        implementation of :class:`django.db.models.Manager` as provided by
        ``calingen_manager`` on all of the app's models. All of these managers
        rely on an app- and model-specific implementation of
        :class:`django.db.models.QuerySet` that provide a model-specific method
        ``filter_by_user()``.

        Returns
        -------
        django.db.models.QuerySet
            The actual returned QuerySet is provided by the model's app-specific
            manager ``calingen_manager``.

        Raises
        ------
        django.core.exceptions.ImproperlyConfigured
            The attribute ``model`` has to be defined on the view.
        """
        if self.model is None:
            raise ImproperlyConfigured(
                "{} is missing the 'model' attribute!".format(self.__class__.__name__)
            )

        return self.model.calingen_manager.get_queryset().filter_by_user(
            self.request.user
        )


class ProfileIDMixin:
    """Injects the :class:`~calingen.models.profile.Profile` id of the ``request.user`` into the context.

    This mixin uses ``get_context_data()`` to inject the ``profile_id``.

    The mixin can safely be used on any ``View`` that also uses the
    :class:`django.contrib.auth.mixins.LoginRequiredMixin`.
    """

    def get_context_data(self, **kwargs):  # noqa: D102
        context = super().get_context_data(**kwargs)

        context["profile_id"] = Profile.calingen_manager.get_profile(
            self.request.user
        ).id

        return context


class AllCalendarEntriesMixin:
    """Add all :class:`~calingen.interfaces.data_exchange.CalendarEntry` of the ``request.user``.

    This mixin uses ``get_context_data()`` to provide all of the user's
    :class:`~calingen.interfaces.data_exchange.CalendarEntry` instances for
    the context.
    """

    def get_context_data(self, **kwargs):  # noqa: D102
        context = super().get_context_data(**kwargs)

        # get the user's profile (required to process plugins)
        profile = Profile.calingen_manager.get_profile(self.request.user)

        all_entries = CalendarEntryList()
        internal_events = Event.calingen_manager.get_calendar_entry_list(
            user=self.request.user, year=context["target_year"]
        )
        plugin_events = profile.resolve(year=context["target_year"])
        all_entries.merge(internal_events)
        all_entries.merge(plugin_events)
        entries = all_entries.sorted()

        context["entries"] = entries

        # Usually, CalingenUserProfileIDMixin provides the (required)
        # profile_id, but as this view fetches the Profile anyway, it will be
        # added manually
        context["profile_id"] = profile.id

        return context
