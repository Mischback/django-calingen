# SPDX-License-Identifier: MIT

""":class:`~calingen.interfaces.plugin_api.LayoutProvider` implementation for various ruled paper outputs.

More or less all of this module's source code is utility code, that is tied
together in :class:`~calingen.contrib.layouts.lineatur.lineatur.LineaturForm`
and actually used in the layout's templates.

This may seem like a lot of boilerplate (and it is, in fact), but it
demonstrates an easy way to actually implement
:ref:`the LayoutProvider's ability to provide a layout specific configuration <calingen-dev-doc-plugins-layoutprovider-label>`
as implemented by
:attr:`calingen.interfaces.plugin_api.LayoutProvider.configuration_form`.
"""

# Django imports
from django.db.models import TextChoices
from django.forms import CharField, ChoiceField, FloatField, IntegerField
from django.utils.translation import gettext_lazy as _

# app imports
from calingen.forms.generation import LayoutConfigurationForm
from calingen.interfaces.plugin_api import LayoutProvider


class PaperSize(TextChoices):
    """Provide choices for the paper sizes."""

    A0 = "paperA0", _("A0 (841mm x 1189mm)")
    A1 = "paperA1", _("A1 (594mm x 841mm)")
    A2 = "paperA2", _("A2 (420mm x 594mm)")
    A3 = "paperA3", _("A3 (297mm x 420mm)")
    A4 = "paperA4", _("A4 (210mm x 297mm)")
    A5 = "paperA5", _("A5 (148mm x 210mm)")
    A6 = "paperA6", _("A6 (105mm x 148mm)")
    A7 = "paperA7", _("A7 (74mm x 105mm)")
    B0 = "paperB0", _("B0 (1000mm x 1414mm)")
    B1 = "paperB1", _("B1 (707mm x 1000mm)")
    B2 = "paperB2", _("B2 (500mm x 707mm)")
    B3 = "paperB3", _("B3 (353mm x 500mm)")
    B4 = "paperB4", _("B4 (250mm x 353mm)")
    B5 = "paperB5", _("B5 (176mm x 250mm)")
    B6 = "paperB6", _("B6 (125mm x 176mm)")
    B7 = "paperB7", _("B7 (88mm x 125mm)")
    LETTER = "paperLetter", _("Letter (8.5in x 11.0in)")
    GOV_LETTER = "paperGovLetter", _("Government Letter (8.0in x 10.5in)")
    LEGAL = "paperLegal", _("Government Legal (8.5in x 14.0in)")
    LEDGER = "paperLedger", _("Ledger (17.0in x 11.0in)")
    TABLOID = "paperTabloid", _("Tabloid (11.0in x 17.0in)")


class LengthUnits(TextChoices):
    """Provide CSS absolute length units.

    Taken from here:
    https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Values_and_units#lengths
    """

    CM = "cm", _("Centimeters")
    MM = "mm", _("Millimeters")
    IN = "in", _("Inches")
    PT = "pt", _("Points (1/72th of 1in)")
    PX = "px", _("Pixels (1/96th of 1in)")


class LineaturTypes(TextChoices):
    """Provide different types of grids."""

    BLANK = "blank", _("blank")
    DOTTED = "dotted", _("dotted")
    LINED = "lined", _("lined")
    SQUARED = "squared", _("squared")


class CaptionPositionChoices(TextChoices):
    """Where to put the caption."""

    LEFT = "left", _("left")
    CENTER = "center", _("center")
    RIGHT = "right", _("right")


class ColorChoices(TextChoices):
    """Pre-defined colors to use in the generated output."""

    BLACK = "rgb(0,0,0)", _("black")
    DARK_GREY = "rgb(64,64,64)", _("dark grey")
    LIGHT_GREY = "rgb(128,128,128)", _("light grey")
    RED = "rgb(255,0,0)", _("red")
    GREEN = "rgb(0,255,0)", _("green")
    BLUE = "rgb(0,0,255)", _("blue")


class LineaturForm(LayoutConfigurationForm):
    """Configuration form for the Lineatur layout.

    This is actually a subclass of
    :class:`calingen.forms.generation.LayoutConfigurationForm` and exposes some
    options to adjust the generated page, e.g. the format of the paper, margins
    and the actual grid.
    """

    template_name = "lineatur/config_form.html"

    caption = CharField(
        label=_("Caption"),
        help_text=_("An optional caption, placed in the specified position"),
        max_length=150,
        required=False,
        empty_value="",
    )

    caption_position = ChoiceField(
        label=_("Position of the Caption"),
        help_text=_("Where to put the caption"),
        choices=CaptionPositionChoices.choices,
        required=True,
        initial=CaptionPositionChoices.RIGHT,
    )

    caption_size = IntegerField(
        label=_("Size of the Caption"),
        help_text=_("Size in pt of the caption"),
        required=True,
        initial=16,
        min_value=1,
    )

    caption_font = CharField(
        label=_("Font Family of the Caption"),
        help_text=_(
            "Specify the font to use; will be passed to a CSS font-family attribute; "
            "You may specify system fonts; default: sans-serif."
        ),
        required="False",
        empty_value="sans-serif",
    )

    caption_color = ChoiceField(
        label=_("Caption Text Color"),
        help_text=_("The color to be used for the caption."),
        choices=ColorChoices.choices,
        required=True,
        initial=ColorChoices.LIGHT_GREY,
    )

    paper_size = ChoiceField(
        label=_("Paper Size"),
        help_text=_("The paper size to be used"),
        choices=PaperSize.choices,
        required=True,
        initial=PaperSize.A5,
    )

    lineatur_type = ChoiceField(
        label=_("Type of Grid to generate"),
        help_text=_("Determine which grid is generated"),
        choices=LineaturTypes.choices,
        required=True,
        initial=LineaturTypes.BLANK,
    )

    length_unit = ChoiceField(
        label=_("Unit of lengths"),
        help_text=_("Determine the unit for specified lengths"),
        choices=LengthUnits.choices,
        required=True,
        initial=LengthUnits.CM,
    )

    lineatur_spacing_x = FloatField(
        label=_("Grid horizontal spacing"),
        help_text=_("The horizontal spacing of the grid. See Unit of lengths."),
        required=True,
        initial=0.5,
    )

    lineatur_spacing_y = FloatField(
        label=_("Grid vertical spacing"),
        help_text=_("The vertical spacing of the grid. See Unit of lengths."),
        required=True,
        initial=0.5,
    )

    lineatur_color = ChoiceField(
        label=_("Grid Color"),
        help_text=_("The color to render the selected grid"),
        choices=ColorChoices.choices,
        required=True,
        initial=ColorChoices.LIGHT_GREY,
    )

    lineatur_stroke_width = IntegerField(
        label=_("Width of the grid strokes"),
        help_text=_("The width of the grid strokes specified in pixels"),
        required=True,
        initial=1,
        min_value=0,
    )

    page_margin_top = FloatField(
        label=_("Margin (top)"),
        help_text=_(
            "Space between the page's and the content's top edges. "
            "See Unit of lengths."
        ),
        required=True,
        initial=0,
    )

    page_margin_right = FloatField(
        label=_("Margin (right)"),
        help_text=_(
            "Space between the page's and the content's right edges. "
            "See Unit of lengths."
        ),
        required=True,
        initial=0,
    )

    page_margin_bottom = FloatField(
        label=_("Margin (bottom)"),
        help_text=_(
            "Space between the page's and the content's bottom edges. "
            "See Unit of lengths."
        ),
        required=True,
        initial=0,
    )

    page_margin_left = FloatField(
        label=_("Margin (left)"),
        help_text=_(
            "Space between the page's and the content's left edges. "
            "See Unit of lengths."
        ),
        required=True,
        initial=0,
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
    _template = "lineatur/layout.html"
