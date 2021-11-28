# SPDX-License-Identifier: MIT

# Django imports
from django.forms.fields import CallableChoiceIterator
from django.forms.widgets import CheckboxSelectMultiple, MultiWidget, TextInput


class PluginWidget(MultiWidget):
    def __init__(self, *args, **kwargs):
        widgets = (CheckboxSelectMultiple(), TextInput())
        super().__init__(widgets=widgets, *args, **kwargs)

    def update_available_plugins(self, choices=()):
        # See: django.forms.fields.ChoiceField._set_choices
        if callable(choices):
            widget_choices = CallableChoiceIterator(choices)
        else:
            widget_choices = list(choices)
        self.widgets[0].choices = widget_choices

    def decompress(self, value):
        if value:
            active = value.get("active", [])
            unavailable = value.get("unavailable", [])
            return [active, unavailable]

        return [None, None]
