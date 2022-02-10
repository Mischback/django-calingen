# SPDX-License-Identifier: MIT

"""Provides the API for plugins."""

# Python imports
from datetime import datetime

# Django imports
from django.template.loader import render_to_string
from django.utils.functional import classproperty

# app imports
from calingen.interfaces.data_exchange import (
    SOURCE_EXTERNAL,
    CalendarEntry,
    CalendarEntryList,
)


def fully_qualified_classname(class_or_instance):
    """Get the fully qualified Python path of a class (or instance).

    Parameters
    ----------
    class_or_instance : any
        The class (or instance of a class) to work on

    Returns
    -------
    str
        The fully qualified, dotted Python path of that class or instance.
    """
    if isinstance(class_or_instance, type):
        # operating on a class (NOT an instance!)
        return ".".join([class_or_instance.__module__, class_or_instance.__qualname__])

    # operating on an instance
    return ".".join(
        [
            class_or_instance.__class__.__module__,
            class_or_instance.__class__.__qualname__,
        ]
    )


class PluginMount(type):
    """Core of the plugin api.

    Notes
    -----
    Searching Google with any Django-related term usually results in at least
    five StackOverflow threads with similar issues. This failed for "django
    plugin system" (ok, there are SO threads, without providing any real
    solution).

    However, there is a blog post by Marty Alchin, dating back to 2008 [1]_,
    describing some sort of `weird Python sorcery`.
    Digging deeper, while trying to understand the purpose and possible
    application of ``metaclass`` in this context, this SO thread [2]_ was found
    (easily one of the best SO threads on a general programming technique).

    Obviously, [1]_ was ported to Python3 syntax (getting rid of ``__metaclass__``
    and apply it in the class definition of the actual mount point).

    References
    ----------
    .. [1] http://martyalchin.com/2008/jan/10/simple-plugin-framework/
    .. [2] https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python
    """

    def __init__(cls, name, bases, attrs):
        """Initialize the plugin list."""
        if not hasattr(cls, "plugins"):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls.plugins = []
        else:
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            cls.plugins.append(cls)


class EventProvider(metaclass=PluginMount):
    """Mount point for plugins that provide events.

    Plugins implementing this reference **must** provide the following attribute:

    - **title** (:py:obj:`str`): The title of the provider, provided as a class
      attribute.

    Plugins implementing this reference **can** provide the following attributes
    and/or methods:

    - **entries** (:py:obj:`list`): A list of
      :class:`calingen.interfaces.data_exchange.CalendarEntry` instances.

      The default implementation of
      :meth:`~calingen.interfaces.plugin_api.EventProvider.resolve` will work
      on this :py:obj:`list`. Alternatively
      :meth:`~calingen.interfaces.plugin_api.EventProvider.resolve` may be
      re-implemented (see below).
    - **resolve(year)** : A classmethod that accepts a **year** (:py:obj:`int`)
      as parameter and returns an instance of
      :class:`calingen.interfaces.data_exchange.CalendarEntryList` containing
      the `Events` of the requested year with their corresponding meta
      information as specified by
      :class:`calingen.interfaces.data_exchange.CalendarEntry`.
    """

    @classmethod
    def list_available_plugins(cls):
        """Return the available plugins.

        Returns
        -------
        set
            The resulting :py:obj:`set` contains a 2-tuple for every plugin,
            including its `qualified classname` and its ``title`` attribute.
            The `qualified classname` is determined by
            :func:`~calingen.interfaces.plugin_api.fully_qualified_classname`.

        Notes
        -----
        Primary use case for this method is the usage in a Django view,
        specifically :class:`~calingen.models.profile.ProfileForm` uses this
        method to provide the choices of its field. That ``Form`` is then used
        in the app's views, e.g. :class:`calingen.views.profile.ProfileUpdateView`.
        """
        result = set()
        for plugin in cls.plugins:
            result.add((fully_qualified_classname(plugin), plugin.title))

        # the ``set`` is sorted on return (converting it to a list, but that's
        # fine with the current (only) consumer)
        return sorted(result, key=lambda plugin_tuple: plugin_tuple[1])

    @classmethod
    def resolve(cls, year):
        """Return a list of events.

        Parameters
        ----------
        year : int
            The year to retrieve the list of events for.

        Returns
        -------
        :class:`calingen.interfaces.data_exchange.CalendarEntryList`
            Wraps the actual events, provided as
            :class:`calingen.interfaces.data_exchange.CalendarEntry` into one
            single object.

        Notes
        -----
        This is the default implementation of the ``resolve()`` method. It makes
        some assumptions about the internal structure of an actual
        implementation of :class:`~calingen.interfaces.plugin_api.EventProvider`:

        - A class variable ``entries`` provides a :py:obj:`list` of
          :py:obj:`tuple` instances with the following structure:
          ``(title, category, recurrence)``:

            - ``title``: :py:obj:`str`
            - ``category``: :py:obj:`str`, but it is recommended to rely on a
              predefined value from :class:`calingen.constants.EventCategory`
            - ``recurrence``: :class:`dateutil.rrule.rrule`

        - A class variable ``title`` (:py:obj:`str`). This is already a required
          parameter of the :class:`~calingen.interfaces.plugin_api.EventProvider`
          implementation itsself and is used to populate the ``source``
          attribute of the returned
          :class:`~calingen.interfaces.data_exchange.CalenderEntry` instances.
        """
        result = CalendarEntryList()
        for entry in cls.entries:
            result.add(
                CalendarEntry(
                    entry[0],
                    entry[1],
                    entry[2].between(
                        datetime(year, 1, 1), datetime(year, 12, 31), inc=True
                    )[0],
                    (SOURCE_EXTERNAL, cls.title),
                )
            )
        return result


class LayoutProvider(metaclass=PluginMount):
    """Mount point for plugins that provide layouts.

    Plugins implementing this reference **must** provide the following
    attributes:

    - **title** (:py:obj:`str`): The ``title`` will be used to represent the
      plugin in the app's views. It **must be** provided as a class attribute
      resolving to a :py:obj:`str`. However, it is recommended to provide the
      following class attributes instead:

        - **name** (:py:obj:`str`): A descriptive name of the layout.
        - **paper_size** (:py:obj:`str`): The size of the paper, e.g. ``"a4"``,
          ``"a5"``, etc.
        - **orientation** (:py:obj:`str`): The orientation, e.g. ``"landscape"``
          or ``"portrait"``.

      By providing these attributes, the ``title`` can be provided automatically
      by :meth:`~calingen.interfaces.plugin_api.LayoutProvider.title` in a
      unified way throughout the application.
    - **layout_type** (:py:obj:`str`): This required class attribute specifies
      the source language of the rendered result and is used in
      :class:`calingen.views.generation.CompilerView` to determine
      which compiler is to be used to actually compile the rendered source to
      its final product.

      The actual mapping of ``layout_type`` to compiler is done in the
      app-specific setting :py:data:`~calingen.settings.CALINGEN_COMPILER`.

      ``layout_type`` may not be ``"default"``, as this is a special key used
      internally in :class:`~calingen.views.generation.CompilerView` and
      specifies the fallback compiler for the case that there is no dedicated
      compiler available for the ``layout_type`` of a layout.

    Plugins implementing this reference **can** provide implementations of the
    following methods:

    - **prepare_context(context)** (:py:obj:`dict`): This method performs
      pre-processing of the ``context``. If an actual layout needs data in a
      different structure than provided by
      :class:`calingen.views.generation.CompilerView`, this method may be
      re-implemented by the actual layout. See
      :meth:`~calingen.interfaces.plugin_api.LayoutProvider.prepare_context` for
      additional details.
    - **render(year, entries)** (:py:obj:`str`): Actually renders the layout's
      templates with the given context. This method may be re-implemented by
      actual layouts, though it is pretty generic as it is and should work for
      most use cases. It calls
      :meth:`~calingen.interfaces.plugin_api.LayoutProvider.prepare_context` for
      pre-processing of the context. It is recommended to rely on
      ``prepare_context()`` in actual layout implementations.
    """

    configuration_form = None
    """Layouts may provide a custom form to fetch configuration values.

    The specified form should be a subclass of
    :class:`calingen.forms.generation.LayoutConfigurationForm` and may implement
    custom validation / cleaning logic.
    """

    @classproperty
    def title(cls):
        """Return the plugin's human-readable title.

        Returns
        -------
        str
            The plugin's title is constructed from class attributes.

        Notes
        -----
        The ``title`` is provided as a
        :class:`~django.utils.functional.classproperty`.

        If an actual layout implementation wishes to provide its title in a
        different way, it may provide a specific implementation of this method
        or provide a plain ``title`` class attribute, resolving to a
        :py:obj:`str` (TODO: NEEDS VERIFICATION!).
        """
        return "{} ({}, {})".format(cls.name, cls.paper_size, cls.orientation)

    @classmethod
    def list_available_plugins(cls):
        """Return the available plugins.

        Returns
        -------
        set
            The resulting :py:obj:`set` contains a 2-tuple for every plugin,
            including its `qualified classname` and its **title** attribute.
            The `qualified classname` is determined by
            :func:`~calingen.interfaces.plugin_api.fully_qualified_classname`.

        Notes
        -----
        Primary use case for this method is the usage in a Django view,
        specifically :class:`~calingen.models.profile.ProfileForm` uses this
        method to provide the choices of its field. That ``Form`` is then used
        in the app's views, e.g. :class:`~calingen.views.profile.ProfileUpdateView`.
        """
        result = set()
        for plugin in cls.plugins:
            result.add((fully_qualified_classname(plugin), plugin.title))

        # the ``set`` is sorted on return (converting it to a list, but that's
        # fine with the current (only) consumer)
        return sorted(result, key=lambda plugin_tuple: plugin_tuple[1])

    @classmethod
    def prepare_context(cls, context):
        """Pre-process the context before rendering.

        Parameters
        ----------
        context : dict
            The context, as provided by
            :meth:`calingen.views.generation.CompilerView.get`.

        Returns
        -------
        dict
            The updated context.

        Notes
        -----
        This default implementation does nothing. ``LayoutProvider``
        implementations may override this method to apply necessary modifications
        of the ``context``.
        """
        return context  # pragma: nocover

    @classmethod
    def render(cls, context, *args, **kwargs):
        """Return the rendered source.

        Returns
        -------
        str
            The rendered source.

        Notes
        -----
        This is a very basic implementation of the (required) ``render()``
        method.
        """
        # Apply a pre-processing step to the context
        context = cls.prepare_context(context)

        return render_to_string(cls._template, context)


class CompilerProvider(metaclass=PluginMount):
    """Mount point for plugins that provide means to compile layouts to documents.

    Plugins implementing this reference **must** provide the following attributes
    and methods:

    - **title** (:py:obj:`str`): The title of the provider.
    - **get_response()** : A classmethod that accepts a :py:obj:`str`, which
      will be the rendered layout source as provided by
      :meth:`LayoutProvider.render() <calingen.interfaces.plugin_api.LayoutProvider.render>`.
      The method **must return** a valid
      :djangoapi:`Django Response object <request-response/#httpresponse-objects>`.
    """

    @classmethod
    def list_available_plugins(cls):
        """Return the available plugins.

        Returns
        -------
        set
            The resulting :py:obj:`set` contains a 2-tuple for every plugin,
            including its `qualified classname` and its **title** attribute.
            The `qualified classname` is determined by
            :func:`~calingen.interfaces.plugin_api.fully_qualified_classname`.
        """
        result = set()
        for plugin in cls.plugins:
            result.add((fully_qualified_classname(plugin), plugin.title))

        # the ``set`` is sorted on return (converting it to a list, but that's
        # fine with the current (only) consumer)
        return sorted(result, key=lambda plugin_tuple: plugin_tuple[1])

    @classmethod
    def get_response(cls, source, *args, **kwargs):
        """Get the compiler's HTTP response.

        This is the compiler's main interface to other components of the app.

        It should be used to actually trigger the compilation of the provided
        source and then return a valid
        :djangoapi:`Django Response object <request-response/#httpresponse-objects>`.

        Parameters
        ----------
        source : str
            The source as provided by
            :meth:`LayoutProvider.render() <calingen.interfaces.plugin_api.LayoutProvider.render>`.

        Returns
        -------
        :djangoapi:`Django Response object <request-response/#httpresponse-objects>`

        Notes
        -----
        This method is called from
        :meth:`CompilerView's get() method <calingen.views.generation.CompilerView.get>`
        with an additional keyword argument ``layout_type``, exposing the
        :attr:`~calingen.interfaces.plugin_api.LayoutProvider.layout_type`
        attribute of the layout.
        """
        raise NotImplementedError(
            "Has to be implemented by the actual provider"
        )  # pragma: nocover
