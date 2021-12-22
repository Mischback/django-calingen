# SPDX-License-Identifier: MIT

"""Provides defaults for the app-specific settings.

This module contains the app-specific settings with their respective default
values.

The settings may be provided in the project's settings module.
"""

# FIXME: Needs renaming!
CALINGEN_TEX_COMPILER = None
"""Set the project's TeX compiler.

**Default value:** ``None``

Warnings
--------
This is a mandatory parameter for project's including
:class:`~calingen.views.generation.CompilerView`.

``None`` is not a valid configuration option here. If you do not want your  project
to provide actual TeX compilation, you may provide the (included)
:class:`~calingen.contrib.compiler.noop.compiler.NoOpCompiler` by providing
``"calingen.contrib.compiler.noop.compiler.NoOpCompiler"`` for this setting.

Notes
-----
Provide a dotted Python path to a
:class:`~calingen.interfaces.plugin_api.CompilerProvider` implementation.
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
