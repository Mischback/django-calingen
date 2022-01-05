# SPDX-License-Identifier: MIT

""":class:`~calingen.interfaces.plugin_api.LayoutProvider` implementation for various ruled paper outputs."""

# Django imports
from django.forms import CharField
from django.utils.translation import gettext_lazy as _

# app imports
from calingen.forms.generation import LayoutConfigurationForm
from calingen.interfaces.plugin_api import LayoutProvider


class LineaturForm(LayoutConfigurationForm):
    """Configuration form for the Lineatur layout.

    This is actually a subclass of
    :class:`calingen.forms.generation.LayoutConfigurationForm` and exposes some
    options to adjust the generated page, e.g. the format of the paper, margins
    and the actual grid.
    """

    caption = CharField(
        label=_("Caption"),
        help_text=_("An optional caption, placed in the top right (outer) corner"),
        max_length=150,
        required=False,
        empty_value="",
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
