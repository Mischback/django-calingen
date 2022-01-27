###############
App's Internals
###############

*********************************************
Django ``models`` and their related ``views``
*********************************************

|calingen| defines only two actual models:
:class:`~calingen.models.profile.Profile` and
:class:`~calingen.models.event.Event`.

:class:`~calingen.models.profile.Profile` is used to store *user-specifc*
settings that are specific to |calingen| (as of now, this is in fact just the
user's selection of
:class:`EventProviders <calingen.interfaces.plugin_api.EventProvider>`).

.. note::
  The user's :class:`~calingen.models.profile.Profile` is tied to his account
  within the actual Django project and each user is limited to only one
  instance of :class:`~calingen.models.profile.Profile`.

  That is a design decision, assuming that |calingen| is used to create one's
  personal calendar pages.

The :class:`Event class <calingen.models.event.Event>` is used to store
*user-provided* entries in his personal calendar. Every instance is tied to
the user's :class:`~calingen.models.profile.Profile`, meaning it may not be
accessed by any other user of the Django project.

.. note::
  Again, that's a design decision, assuming that |calingen| is used to create
  one's personal calendar pages.

  For implementation details, refer to
  :ref:`calingen-dev-doc-permission-system-label`.

  If you are interested in *sharing* calendar entries between different users
  of the Django project, have a look at
  :ref:`calingen-cookbook-sharing-events-label`.

Both models are accessible with basic *CRUD* operations (*create*, *retrieve*,
*update*, *delete*). Implementationwise these operations are based on Django's
generic Class Based Views (CBV), with app-specific extensions to support
:ref:`calingen-dev-doc-permission-system-label`,

The following image visualizes the involved elements using the example of
:class:`~calingen.models.event.Event` and the corresponding view to update
those objects, :class:`~calingen.views.event.EventUpdateView`. The principles
are applicable to other ``Event``-related views and
:class:`~calingen.models.profile.Profile` and its views.

.. graphviz:: /includes/event_crud.dot

:class:`~calingen.views.event.EventUpdateView` inherit its basic functionality
from :class:`django.views.generic.edit.UpdateView`. Additionally, in order to
enable :ref:`calingen-dev-doc-permission-system-label`,
:class:`~calingen.views.mixins.RestrictToUserMixin` ensures, that the
app-specific :attr:`~calingen.models.event.Event.calingen_manager` is used to
retrieve :class:`~calingen.models.event.Event` instances (using
:class:`~calingen.models.event.EventManager`).

:class:`~calingen.views.event.EventUpdateView` also ensures, that the
model-specific :class:`~calingen.models.event.EventForm` is used to update the
instance.

This concept is applied - with slight variations - to all *CRUD-related views*:

- :class:`~calingen.views.event.EventCreateView`: Does not use
  the :class:`~calingen.views.mixins.RestrictToUserMixin`, as it handles a
  *not yet existing* instance.
- :class:`~calingen.views.event.EventDetailView` and
  :class:`~calingen.views.event.EventListView` do not use
  :class:`~calingen.models.event.EventForm`, as these views do simply not work
  with any form.
- :class:`~calingen.views.event.EvendDeleteView` does use a ``Form``
  internally, but not corresponding to
  :class:`~calingen.models.event.EventForm` (actually this is left to Django).

The implementation for :class:`~calingen.models.profile.Profile` is pretty
much identical, with the exception that there is no ``ProfileListView``,
because every user only have exactly one associated
:class:`~calingen.models.profile.Profile`.


.. _calingen-dev-doc-permission-system-label:

***************************************
``django-calingen``'s Permission System
***************************************

Django's built-in
:djangodoc:`Permissions<topics/auth/default/#permissions-and-authorization>`
are working on *model level*, meaning that if a project's user is permitted to
view, create, update or delete a given *model*, he may tinker with all
instances of that model.

For |calingen|, that would mean, that any user of the Django project may view,
update or delete any instance of :class:`~calingen.models.event.Event`, even
the ones of other users.

Obviously, that is not the desired behaviour.

.. important::
  **TODO**: And now describe how this is solved using custom model managers
  and view mixins

  Include a warning, that these permissions have **no effect** in Django's
  admin interface, so the project's administrator can see everything!


.. |calingen| replace:: **django-calingen**
