# SPDX-License-Identifier: MIT

"""App-specific implementation of :class:`django.db.models.QuerySet`."""


# Django imports
from django.db.models import QuerySet


class CalingenQuerySet(QuerySet):
    """Base class for all app-specific ``QuerySet`` implementations.

    Notes
    -----
    This :class:`~django.db.models.QuerySet` implementation provides
    app-specific augmentations, most notable the ability to filter the resulting
    set by the class's ``owner`` attribute, which is a reference to
    :setting:`AUTH_USER_MODEL`.

    The app's :class:`~django.db.models.QuerySet` implementations are applied
    by the model's specific implementation of :class:`django.db.models.Manager`,
    which is available as attribute ``calingen_manager`` on every model of the
    `calingen` app.
    """

    def default(self):
        """Return a queryset with annotations.

        Returns
        -------
        :class:`django.db.models.QuerySet`
            The annotated queryset.

        Warnings
        --------
        Currently, this method does nothing on its own, but is kept to keep the
        app's specific QuerySets consistent.
        """
        return self  # pragma: nocover

    def filter_by_user(self, user):
        """Return a queryset filtered by the ``owner`` attribute.

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
        raise NotImplementedError(
            "Must be implemented by actual QuerySet"
        )  # pragma: nocover
