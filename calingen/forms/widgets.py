# SPDX-License-Identifier: MIT

# Python imports
import logging

# Django imports
from django.forms.fields import CallableChoiceIterator
from django.forms.widgets import CheckboxSelectMultiple, MultiWidget, TextInput

logger = logging.getLogger(__name__)


class CalingenCheckboxSelectMultiple(CheckboxSelectMultiple):
    def __init__(self, *args, choices=(), **kwargs):
        logger.debug("running CalingenCheckboxSelectMultiple.__init__()")

        super().__init__(*args, **kwargs)


class CalingenTextInput(TextInput):
    def __init__(self, *args, **kwargs):
        logger.debug("CalingenTextInput.__init__()")

        super().__init__(*args, **kwargs)


class PluginWidget(MultiWidget):
    def __init__(self, *args, **kwargs):
        logger.debug("running PluginWidget.__init__()")

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
