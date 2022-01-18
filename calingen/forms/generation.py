# SPDX-License-Identifier: MIT

"""Implementations of :class:`django.forms.Form` in the context of rendering and compilation."""

# Python imports
from datetime import date

# Django imports
from django.forms.fields import ChoiceField, IntegerField
from django.forms.widgets import RadioSelect
from django.utils.translation import gettext_lazy as _

# app imports
from calingen.forms.generic import RequestEnabledForm
from calingen.interfaces.plugin_api import LayoutProvider


class LayoutConfigurationForm(RequestEnabledForm):
    """Layout-specific configuration form.

    Implementations of :class:`calingen.interfaces.plugin_api.LayoutProvider`
    may provide a subclass of this form to fetch layout-specific configuration
    values during the rendering process of a layout.

    Warnings
    --------
    To make this work, the Django project must provide support for
    :djangodoc:`Django's Sessions <topics/http/sessions/>`. This is in fact
    verified by :func:`calingen.checks.check_session_enabled`.

    Notes
    -----
    For an example usage, see :class:`calingen.contrib.layouts.lineatur.lineatur.LineaturForm`.
    """

    def save_configuration(self):
        """Save the layout-specific configuration in the user's ``Session``."""
        self.request.session[
            "layout_configuration"
        ] = self.cleaned_data  # pragma: nocover


class LayoutSelectionForm(RequestEnabledForm):
    """Select one of the available :class:`~calingen.interfaces.plugin_api.LayoutProvider` instances.

    Warnings
    --------
    To make this work, the Django project must provide support for
    :djangodoc:`Django's Sessions <topics/http/sessions/>`. This is in fact
    verified by :func:`calingen.checks.check_session_enabled`.

    Notes
    -----
    As all layouts require a ``target_year``, this is included here aswell.
    """

    target_year = IntegerField(
        label=_("Year"),
        help_text=_("The year to generate the layout for"),
        initial=date.today().year + 1,
        min_value=date.min.year,
        max_value=date.max.year,
    )
    """Specify the year to create the layout for."""

    layout = ChoiceField(
        label=_("Layout"),
        help_text=_("Select the layout to be used"),
        choices=LayoutProvider.list_available_plugins,
        widget=RadioSelect,
    )
    """Presentation of the available :class:`~calingen.interfaces.plugin_api.LayoutProvider`.

    Notes
    -----
    The available ``LayoutProvider`` are determined dynamically by calling
    :meth:`LayoutProvider.list_available_plugins() <calingen.interfaces.plugin_api.LayoutProvider.list_available_plugins>`
    and presented using a :class:`~django.forms.widgets.RadioSelect` widget.
    """

    def save_selection(self):
        """Save the layout selection in the user's ``Session``."""
        self.request.session["target_year"] = self.cleaned_data[
            "target_year"
        ]  # pragma: nocover
        self.request.session["selected_layout"] = self.cleaned_data[
            "layout"
        ]  # pragma: nocover
