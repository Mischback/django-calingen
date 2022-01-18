# SPDX-License-Identifier: MIT

"""App-specific implementations of :class:`django.forms.widgets.Widget`."""

# Django imports
from django.forms.fields import CallableChoiceIterator
from django.forms.widgets import CheckboxSelectMultiple, HiddenInput, MultiWidget


class PluginWidget(MultiWidget):
    """Widget to render the app-specific :class:`~calingen.forms.fields.plugin.PluginField`."""

    def __init__(self, *args, **kwargs):
        widgets = (CheckboxSelectMultiple(), HiddenInput())
        super().__init__(widgets=widgets, *args, **kwargs)

    def update_available_plugins(self, choices=()):
        """Apply the choices to the multiple choice checkbox field.

        Notes
        -----
        In a normal, 1:1 relation of fields and widgets, this happens
        automatically during widget initialisation. However, using
        :class:`~django.forms.fields.MultiValueField` and
        :class:`~django.forms.widgets.MultiWidget`, this step is not performed
        for the subwidgets.

        The constructor of :class:`~calingen.forms.fields.PluginField` will take
        care of this by calling this method.
        """
        # See: django.forms.fields.ChoiceField._set_choices
        if callable(choices):
            widget_choices = CallableChoiceIterator(choices)
        else:
            widget_choices = list(choices)
        self.widgets[0].choices = widget_choices

    def decompress(self, value):
        """Expand the received value to render its components in different widgets.

        Notes
        -----
        See the corresponding :meth:`calingen.forms.fields.PluginField.compress`
        method.
        """
        if value:
            active = value.get("active", [])
            unavailable = value.get("unavailable", [])
            return [active, unavailable]

        return [None, None]
