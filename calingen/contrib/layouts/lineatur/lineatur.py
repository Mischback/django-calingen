# SPDX-License-Identifier: MIT

""":class:`~calingen.interfaces.plugin_api.LayoutProvider` implementation for various ruled paper outputs."""

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
    PX = "px", _("Pixels (1/96th of 1in")


class LineaturTypes(TextChoices):
    """Provide different types of grids."""

    BLANK = "blank", _("blank")
    # DOTTED = "dotted", _("dotted")
    # LINED = "lined", _("lined")
    SQUARED = "squared", _("squared")


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

    lineatur_spacing_x = FloatField(
        label=_("Grid horizontal spacing"),
        help_text=_("The horizontal spacing of the grid"),
        required=True,
        initial=0.5,
    )

    lineatur_spacing_y = FloatField(
        label=_("Grid vertical spacing"),
        help_text=_("The vertical spacing of the grid"),
        required=True,
        initial=0.5,
    )

    lineatur_stroke_width = IntegerField(
        label=_("Width of the grid strokes"),
        help_text=_("The width of the grid strokes specified in pixels"),
        required=True,
        initial=1,
        min_value=0,
    )

    length_unit = ChoiceField(
        label=_("Unit of lengths"),
        help_text=_("Determine the unit for specified lengths"),
        choices=LengthUnits.choices,
        required=True,
        initial=LengthUnits.CM,
    )

    page_margin_top = FloatField(
        label=_("Margin (top)"),
        help_text=_("Space between the page's and the content's top edges"),
        required=True,
        initial=0,
    )

    page_margin_right = FloatField(
        label=_("Margin (right)"),
        help_text=_("Space between the page's and the content's right edges"),
        required=True,
        initial=0,
    )

    page_margin_bottom = FloatField(
        label=_("Margin (bottom)"),
        help_text=_("Space between the page's and the content's bottom edges"),
        required=True,
        initial=0,
    )

    page_margin_left = FloatField(
        label=_("Margin (left)"),
        help_text=_("Space between the page's and the content's top edges"),
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
    _template = "lineatur/base.html"
