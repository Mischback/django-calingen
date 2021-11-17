# SPDX-License-Identifier: MIT

"""Provides app-specific mixins to be used with class-based views."""

# Django imports
from django.core.exceptions import ImproperlyConfigured


class CalingenRestrictToUserMixin:
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
