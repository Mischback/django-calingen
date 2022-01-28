###############
App's Internals
###############

.. _calingen-dev-doc-crud-views-label:

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
generic
:djangodoc:`Class Based Views <topics/class-based-views/generic-editing/>`
(CBV), with app-specific extensions to support
:ref:`calingen-dev-doc-permission-system-label`,

The following image visualizes the involved elements using the example of
:class:`~calingen.models.event.Event` and the corresponding view to update
those objects, :class:`~calingen.views.event.EventUpdateView`. The principles
are applicable to other ``Event``-related views and
:class:`~calingen.models.profile.Profile` and its views.

.. graphviz:: /includes/event_crud.dot
  :alt: Example of CRUD-operations for Event with EventUpdateView
  :caption: Visualization of EventUpdateView

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

The implementation for the :class:`~calingen.models.profile.Profile` model is
pretty much identical, with the exception that there is no ``ProfileListView``,
because every user only have exactly one associated instance of
:class:`~calingen.models.profile.Profile`.


.. _calingen-dev-doc-permission-system-label:

***************************************
``django-calingen``'s Permission System
***************************************

Django's built-in |Permission System| is working on *model level*, meaning that
if a project's user is permitted to view, create, update or delete a given
*model*, he may tinker with all instances of that model.

For |calingen|, that would mean, that any user of the Django project may view,
update or delete any instance of :class:`~calingen.models.event.Event`, even
the ones of other users.

Obviously, that is not the desired behaviour.

Instead, the app's views ensure that a user can only access *objects owned by
himself*, meaning:

- He may only access the instance of :class:`~calingen.models.profile.Profile`
  that is associated with his account within the project (by default this is an
  instance of :class:`django.contrib.auth.models.User` but internally
  :attr:`Profile.owner <calingen.models.profile.Profile.owner>` is referencing
  :setting:`AUTH_USER_MODEL`; this makes the app pluggable, even if a project
  uses a custom user model, see |Referencing the User Model|).
- He may only access instances of :class:`~calingen.models.event.Event` that
  are tied to his :class:`~calingen.models.profile.Profile` (as provided by
  :attr:`Event.profile <calingen.models.event.Event.profile>`).

.. note::
  Actually this is not really a *permission system*, but rather a *restriction
  system*, limiting what a user can access.

  It is not possible to *share* objects between users of the project. Please
  refer to :ref:`calingen-cookbook-sharing-events-label` for further details.

The following image visualizes the mechanism:

.. graphviz:: /includes/permission_system.dot
  :alt: Displays which classes are involved in the implementation
  :caption: Visualization of the Permission implementation

For model-specific **CRUD views** (see
:ref:`calingen-dev-doc-crud-views-label`), the row-level permissions are
enforced by :class:`~calingen.views.mixins.RestrictToUserMixin`.
:class:`~calingen.views.event.EventUpdateView` is used in the visualization,
but the concept is applicable to all views inheriting from one of Django's
built-in Class-Based Views (CBV),
|that are intended to work with models / objects|.

Internally, all of them use a method ``get_queryset()`` to determine the
instance of :class:`django.db.models.query.QuerySet` to use in order to
retrieve objects from the database (see
:meth:`django.views.generic.list.MultipleObjectMixin.get_queryset` and
:meth:`django.views.generic.detail.SingleObjectMixin.get_queryset` for the
actual implementation details).

However, with the app-specific
:class:`~calingen.views.mixins.RestrictToUserMixin` that method is overwritten
to use the (app-specific) implementation of
:class:`django.db.models.manager.Manager`, which is accessible as a
:djangodoc:`custom model manager <topics/db/managers/#custom-managers>`
provided with the ``calingen_manager`` attribute (see
:attr:`calingen.models.event.Event.calingen_manager` for implementation
details).

The ``calingen_manager`` (e.g.
:attr:`calingen.models.event.Event.calingen_manager`) is also used by other
views of the app, that access the app's models. The visualization includes
:class:`~calingen.views.web.CalendarEntryListView` as an example. It inherits
its ``get_context_data()`` method from
:class:`~calingen.views.mixins.AllCalendarEntriesMixin`, which internally uses
the (app-specific) implementations of :class:`django.db.models.manager.Manager`
provided with the ``calingen_manager`` attribute.

This app- and model-specific ``Manager`` implementation uses a model-specific
implementation of  :class:`django.db.models.query.QuerySet`, which provides a
:meth:`~calingen.models.event.EventQuerySet.filter_by_user` method. This method
is used to provide a filtered sub set of the original ``QuerySet`` to
:class:`django.views.generic.detail.SingleObjectMixin`,
:class:`django.views.generic.list.MultipleObjectMixin` and other app-specific
views, effectively achieving the desired result:

**A user can only retrieve, update and delete objects
that are associated with his account**.

.. warning::
  Please be aware, that the app-specific permission system is implemented by
  providing an **additional** :class:`~django.db.models.manager.Manager` to
  the models.

  In Django's administration backend the app's models are accessed using the
  **default manager**, which is Django's default implementation of
  :class:`~django.db.models.manager.Manager` and
  :class:`~django.db.models.query.QuerySet`, thus, administrators will have
  access to *all objects of every user*.


.. |Permission System| replace:: :djangodoc:`Permission System <topics/auth/default/#permissions-and-authorization>`
.. |Referencing the User Model| replace:: :djangodoc:`Referencing the User Model <topics/auth/customizing/#referencing-the-user-model>`
.. |that are intended to work with models / objects| replace:: :djangodoc:`that are intended to work with models / objects <topics/class-based-views/generic-display/#generic-views-of-objects>`


.. _calingen-dev-doc-layout-rendering-compilation-label:

********************************
Layout Rendering and Compilation
********************************

This is the core functionality of the app.

The following image visualizes the process on an abstract level, before diving
deeper into the implementation details.

.. graphviz:: /includes/layout_process.dot
  :alt: The layout rendering and compilation process
  :caption: Visualization of the Process


.. |calingen| replace:: **django-calingen**
