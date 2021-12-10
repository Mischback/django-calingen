# SPDX-License-Identifier: MIT

""":class:`~calingen.interfaces.plugin_api.LayoutProvider` implementation for a simple event list."""

# app imports
from calingen.interfaces.plugin_api import LayoutProvider


class SimpleEventList(LayoutProvider):
    """A very simple implementation of a list of events."""

    name = "Simple Event List"
    paper_size = "a4"
    orientation = "portrait"
    _template = "calingen/tex/simple_event_list/simple_event_list.tex"
