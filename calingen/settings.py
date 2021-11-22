# SPDX-License-Identifier: MIT

"""Provides defaults for the app-specific settings.

This module contains the app-specific settings with their respective default
values.

The settings may be provided in the project's settings module.
"""

CALINGEN_EXTERNAL_EVENT_PROVIDER = []
"""Determines the available event providers.

**Default value:** ``[]``

Notes
-----
Include dotted Python paths to event provider implementations as :py:obj`str`.
"""
