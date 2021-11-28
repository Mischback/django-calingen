# SPDX-License-Identifier: MIT

# Django imports
from django.forms.fields import CharField, MultipleChoiceField, MultiValueField

# app imports
from calingen.forms.widgets import PluginWidget


class CalingenListField(CharField):
    def prepare_value(self, value):
        return ", ".join(value)

    def to_python(self, value):
        if not value:
            return []

        return [item.strip() for item in value.split(",")]


class PluginField(MultiValueField):

    widget = PluginWidget

    def __init__(self, *args, choices=(), **kwargs):
        self.choices = choices

        fields = (MultipleChoiceField(), CalingenListField())

        super().__init__(fields=fields, *args, **kwargs)

        self.fields[0].choices = self.choices
        self.widget.update_available_plugins(self.choices)

    def prepare_value(self, value):
        prepared_list_field = self.fields[1].prepare_value(value["unavailable"])
        value["unavailable"] = prepared_list_field

        return super().prepare_value(value)

    def compress(self, data_list):
        if data_list:
            result = {}
            result["active"] = data_list[0]
            result["unavailable"] = data_list[1]
            return result
        return None
