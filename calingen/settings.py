# SPDX-License-Identifier: MIT

"""Provides defaults for the app-specific settings.

This module contains the app-specific settings with their respective default
values.

The settings may be provided in the project's settings module.
"""

CALINGEN_COMPILER = {
    "default": "calingen.contrib.compilers.copy_paste.compiler.CopyPasteCompiler",
}
"""Configuration of the compiler plugins.

This setting determines the mapping of available instances of
:class:`~calingen.interfaces.plugin_api.CompilerProvider` and their association
with source files, as determined by ``layout_type`` provided by implementations
of :class:`~calingen.interfaces.plugin_api.LayoutProvider`.

**Default value:** ``{ "default": "calingen.contrib.compilers.copy_paste.compiler.CopyPasteCompiler" }``

Notes
-----
More mappings may be added by specifying this setting in a project's settings
module.

The accepted *keys* are of type :py:obj:`str` and should match whatever the
project's layouts (that is: implementations of
:class:`calingen.interfaces.plugin_api.LayoutProvider`) provide with their
respective ``layout_type`` attributes. If a given ``layout_type`` is not found
in this setting, the ``default`` compiler is used.

The expected *values* are of type :py:obj:`str` and should specify a dotted
Python path to an implementation of
:class:`calingen.interfaces.plugin_api.CompilerProvider`.

This setting is evaluated in :class:`calingen.views.generation.CompilerView`.
"""

CALINGEN_EXTERNAL_EVENT_PROVIDER = []
"""Determines the available event providers.

**Default value:** ``[]``

Notes
-----
Include dotted Python paths to event provider implementations as :py:obj`str`.
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
the corresponding contributions to Django's check framework.
"""
