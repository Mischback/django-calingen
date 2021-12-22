# SPDX-License-Identifier: MIT

"""Provide Form implementations in the context of rendering and compilation."""

# Python imports
from datetime import date

# Django imports
from django.forms.fields import ChoiceField, IntegerField
from django.forms.widgets import RadioSelect

# app imports
from calingen.forms.generic import RequestEnabledForm
from calingen.interfaces.plugin_api import LayoutProvider


class LayoutConfigurationForm(RequestEnabledForm):
    """Layout-specific configuration form.

    Implementations of :class:`calingen.interfaces.plugin_api.LayoutProvider`
    may provide a subclass of this form to fetch layout-specific configuration
    values during the rendering process of a layout.
    """

    def save_configuration(self):
        """Save the layout-specific configuration in the user's ``Session``."""
        self.request.session[
            "layout_configuration"
        ] = self.cleaned_data  # pragma: nocover


class LayoutSelectionForm(RequestEnabledForm):
    """Select one of the available :class:`~calingen.interfaces.plugin_api.LayoutProvider` instances."""

    target_year = IntegerField(
        initial=date.today().year + 1, min_value=date.min.year, max_value=date.max.year
    )
    """Specify the year to create the layout for."""

    layout = ChoiceField(
        choices=LayoutProvider.list_available_plugins, widget=RadioSelect
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