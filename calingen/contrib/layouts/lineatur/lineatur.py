# SPDX-License-Identifier: MIT

""":class:`~calingen.interfaces.plugin_api.LayoutProvider` implementation for various ruled paper outputs."""

# Django imports
from django.forms import CharField

# app imports
from calingen.forms.generation import LayoutConfigurationForm
from calingen.interfaces.plugin_api import LayoutProvider


class LineaturForm(LayoutConfigurationForm):  # noqa: D101
    caption = CharField(
        max_length=150, required=False, empty_value="", help_text="to be done"
    )


class Lineatur(LayoutProvider):
    """Provide different kinds of ruled paper.

    The term *lineatur* can be translated (loosely) to *ruled paper*. It
    describes the lines or grids on paper, usually used for notes.
    """

    name = "Lineatur"
    paper_size = "various"
    orientation = "portrait"
    layout_type = "html"
    configuration_form = LineaturForm
    _template = "lineatur/base.html"
