# SPDX-License-Identifier: MIT

"""App-specific settings with their default values.

Notes
-----
These *(app-specific)* settings are *injected* into the project's ``settings``
module during startup, see this StackOverflow answer [1]_ for the general idea
and :meth:`calingen.apps.CalingenConfig.ready` for implementation details.

The actual settings are defined here with their respective default value. This
module serves as the single source of truth about app-specific settings, meaning
it defines the settings' names, as they will be used in other components of the
app.

During runtime, all settings are **read** from ``django.conf.settings`` - which
is effectively the project's ``settings`` module.

:meth:`calingen.apps.CalingenConfig.ready` checks the presence of all
app-specific settings in the project's ``settings`` module and will inject the
default values as defined in this module, if the setting is missing.

If the setting is already present in the project's ``settings`` module, it will
not be modified.

References
----------
.. [1] https://stackoverflow.com/a/47154840
"""

CALINGEN_COMPILER = {
    "default": "calingen.contrib.compilers.copy_paste.compiler.CopyPasteCompiler",
}
"""Configuration of the compiler plugins.

This setting determines the mapping of available instances of
:class:`~calingen.interfaces.plugin_api.CompilerProvider` and their association
with source files, as determined by ``layout_type`` provided by implementations
of :class:`calingen.interfaces.plugin_api.LayoutProvider`.

**Default value:** ``{ "default": "calingen.contrib.compilers.copy_paste.compiler.CopyPasteCompiler" }``

Notes
-----
More mappings may be added by specifying this setting in a project's settings
module.

The accepted *keys* are of type :py:obj:`str` and should match whatever the
project's layouts (that is: implementations of
:class:`~calingen.interfaces.plugin_api.LayoutProvider`) provide with their
respective ``layout_type`` attributes. If a given ``layout_type`` is not found
in this setting, the ``default`` compiler is used.

The expected *values* are of type :py:obj:`str` and should specify a dotted
Python path to an implementation of
:class:`calingen.interfaces.plugin_api.CompilerProvider`.

This setting is evaluated in :class:`calingen.views.generation.CompilerView`.

:func:`calingen.checks.check_config_value_compiler` verifies the presence of a
``"default"`` compiler **and** that the specified *default compiler* is
importable.
"""

CALINGEN_MISSING_EVENT_PROVIDER_NOTIFICATION = None
"""Determines, if the user should be notified about missing event providers.

**Default value:** ``None``

**Accepted values**: ``None``. ``"messages"``

Notes
-----
The user may activate implementations of
:class:`~calingen.interfaces.plugin_api.EventProvider` in his
:class:`~calingen.models.profile.Profile`. These events will then get included
while generating his calendar inlays.

However, the administrator may choose to disable certain plugins _after_ the
user has activated them. The corresponding ``EventProvider`` will then not be
available.

When the user visits his :class:`~calingen.models.profile.Profile`, he can only
select those ``EventProvider``, which are currently activated by the
administrator. Formerly activated plugins are hidden - **but still stored in
the profile instance**.

This setting controls, if the user is notified about the deactivation of a
formerly selected ``EventProvider`` using Django's ``messages`` framework.

See :meth:`calingen.views.profile.ProfileUpdateView.get_context_data` for
implementation details.

See :func:`calingen.checks.check_config_value_event_provider_notification` for
the corresponding contribution to Django's check framework.
"""
