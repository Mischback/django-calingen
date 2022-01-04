# SPDX-License-Identifier: MIT

""":class:`~calingen.interfaces.plugin_api.LayoutProvider` implementation for various ruled paper outputs."""

# app imports
from calingen.interfaces.plugin_api import LayoutProvider


class Lineatur(LayoutProvider):
    """Provide different kinds of ruled paper.

    The term *lineatur* can be translated (loosely) to *ruled paper*. It
    describes the lines or grids on paper, usually used for notes.
    """

    name = "Lineatur"
    paper_size = "various"
    orientation = "portrait"
    layout_type = "html"
    _template = "lineatur/base.html"
