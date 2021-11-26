# SPDX-License-Identifier: MIT


# Python imports
import logging

# Django imports
from django.forms.fields import CharField, MultipleChoiceField, MultiValueField

# app imports
from calingen.forms.widgets import PluginWidget

logger = logging.getLogger(__name__)


class CalingenMultipleChoiceField(MultipleChoiceField):
    def __init__(self, *args, choices=(), **kwargs):
        logger.debug("running CalingenMultipleChoiceField.__init__()")

        super().__init__(*args, **kwargs)

    def prepare_value(self, value):
        logger.debug("CalingenMultipleChoiceField.prepare_value()")
        return super().prepare_value(value)


class CalingenListField(CharField):

    def __init__(self, *args, **kwargs):
        logger.debug("CalingenListField.__init__()")

        super().__init__(*args, **kwargs)

    def prepare_value(self, value):
        logger.debug("CalingenListField.prepare_value()")
        return ", ".join(value)

    def to_python(self, value):
        logger.debug("CalingenListField.to_python()")
        logger.debug(value)
        if not value:
            return []

        return [item.strip() for item in value.split(",")]


class PluginField(MultiValueField):

    widget = PluginWidget

    def __init__(self, *args, choices=(), **kwargs):
        logger.debug("running PluginField.__init__()")
        self.choices = choices

        fields = (MultipleChoiceField(), CalingenListField())

        super().__init__(fields=fields, *args, **kwargs)

        self.fields[0].choices = self.choices
        self.widget.update_available_plugins(self.choices)

    def compress(self, data_list):
        if data_list:
            result = {}
            result["active"] = data_list[0]
            result["unavailable"] = data_list[1]
            return result
        return None
