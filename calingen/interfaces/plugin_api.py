# SPDX-License-Identifier: MIT

"""Provides the API for plugins."""


class PluginMount(type):
    """Core of the plugin api.

    Notes
    -----
    Searching Google with any Django-related term usually results in at least
    five StackOverflow threads with similar issues. This failed for "django
    plugin system" (ok, there are SO threads, without providing any real
    solution).

    However, there is [1]_, describing some sort of _weird Python sorcery_.
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

    Plugins implementing this reference must provide the following attributes:

    - title : The title of the provider.
    """
