# SPDX-License-Identifier: MIT

"""Provide Form implementations in the context of TeX rendering and compilation."""

# Django imports
from django.forms import Form
from django.forms.fields import ChoiceField
from django.forms.widgets import RadioSelect

# app imports
from calingen.interfaces.plugin_api import LayoutProvider


class TeXLayoutSelectionForm(Form):
    """Select one of the available :class:`~calingen.interfaces.plugin_api.LayoutProvider` instances."""

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

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def save_selection(self):
        """Save the layout selection in the user's ``Session``."""
        self.request.session["selected_layout"] = self.cleaned_data["layout"]
