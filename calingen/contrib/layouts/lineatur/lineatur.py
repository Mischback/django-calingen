# SPDX-License-Identifier: MIT

""":class:`~calingen.interfaces.plugin_api.LayoutProvider` implementation for various ruled paper outputs."""

# app imports
from calingen.interfaces.plugin_api import LayoutProvider


class Lineatur(LayoutProvider):
    """A very simple implementation of a list of events."""

    name = "Lineatur"
    paper_size = "various"
    orientation = "portrait"
    layout_type = "html"
    _template = "lineatur/base.html"
