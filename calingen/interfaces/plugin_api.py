# SPDX-License-Identifier: MIT

"""Provides the API for plugins."""

# Django imports
from django.template.loader import render_to_string
from django.utils.functional import classproperty


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

    Plugins implementing this reference must provide the following attributes
    and methods:

    - **title** : The title of the provider, provided as :py:obj:`str`.
    - **resolve(year)** : A classmethod that accepts a **year** (:py:obj:`int`)
      as parameter and returns an instance of
      :class:`calingen.interfaces.data_exchange.CalenderEntryList` containing
      the `Events` of the requested year with their corresponding meta
      information as specified by
      :class:`calingen.interfaces.data_exchange.CalenderEntry`.
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
    def resolve(cls, year):
        """Return a list of events.

        Parameters
        ----------
        year : int
            The year to retrieve the list of events for.

        Returns
        -------
        :class:`calingen.interfaces.data_exchange.CalenderEntryList`
            Wraps the actual events, provided as
            :class:`calingen.interfaces.data_exchange.CalenderEntry` into one
            single object.

        Notes
        -----
        Neither :class:`~calingen.interfaces.data_exchange.CalenderEntry` nor
        :class:`~calingen.interfaces.data_exchange.CalenderEntryList` perform
        any validation on its data. Don't sticking to the specified and expected
        types will crash later and _might_ be hard to debug.
        """
        raise NotImplementedError(
            "Has to be implemented by the actual provider"
        )  # pragma: nocover


class LayoutProvider(metaclass=PluginMount):
    """Mount point for plugins that provide layouts.

    Plugins implementing this reference must provide the following methods:

    - **render(year, entries)**: Actually renders the layout's templates with
      the given context.

    Plugins implementing this reference should provide the following attributes:

    - **name**: A descriptive name of the layout, provided as :py:obj:`str`.
    - **paper_size**: The size of the paper, provided as :py:obj:`str`, e.g.
      ``"a4"``, ``"a5"``, etc.
    - **orientation**: The orientation, provided as :py:obj:`str`, e.g.
      ``"landscape"`` or ``"portrait"``.
    """

    configuration_form = None
    """Layouts may provide a custom form to fetch configuration values.

    The specified form should be a subclass of
    :class:`calingen.forms.tex.TeXLayoutConfigurationForm` and may implement
    custom validation / cleaning logic.
    """

    @classproperty
    def title(cls):
        """Return the available plugins.

        Returns
        -------
        str
            The plugin's title is constructed from class attributes.

        Notes
        -----
        The ``title`` is provided as a
        :class:`~django.utils.functional.classproperty`.

        If an actual layout implementation wishes to provide its title in a
        different way, it may provide a specific implementation of this method.
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
            :meth:`calingen.views.tex.TeXGeneratorView.get`.

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
        """Return the rendered TeX source.

        Returns
        -------
        str
            The rendered TeX source.

        Notes
        -----
        This is a very basic implementation of the (required) ``render()``
        method.
        """
        # Apply a pre-processing step to the context
        context = cls.prepare_context(context)

        return render_to_string(cls._template, context)


class TeXCompilerProvider(metaclass=PluginMount):
    """Mount point for plugins that provide means to compile TeX to documents.

    Plugins implementing this reference must provide the following attributes
    and methods:

    - **title** : The title of the provider, provided as :py:obj:`str`.
    - **get_response()** : A classmethod that accepts a :py:obj:`str`, which
      will be the rendered TeX layout as provided by
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
    def get_response(cls, tex_source):
        """Get the compiler's HTTP response.

        This is the compiler's main interface to other components of the app.

        It should be used to actually trigger the compilation of the provided
        TeX source and then return a valid
        :djangoapi:`Django Response object <request-response/#httpresponse-objects>`.

        Parameters
        ----------
        tex_source : str
            The TeX source as provided by
            :meth:`LayoutProvider.render() <calingen.interfaces.plugin_api.LayoutProvider.render>`.

        Returns
        -------
        :djangoapi:`Django Response object <request-response/#httpresponse-objects>`

        Notes
        -----
        This method is called from
        :meth:`TeXGeneratorView's get() method <calingen.views.tex.TeXGeneratorView.get>`.
        """
        raise NotImplementedError(
            "Has to be implemented by the actual provider"
        )  # pragma: nocover
