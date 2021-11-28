# SPDX-License-Identifier: MIT

"""Provide a Django form field to manage plugins."""

# Django imports
from django.forms.fields import CharField, MultipleChoiceField, MultiValueField

# app imports
from calingen.forms.widgets import PluginWidget


class CalingenListField(CharField):
    """Misuse a ``CharField`` to handle a list of strings."""

    def prepare_value(self, value):
        """Create a comma seperated list of strings from a Python list.

        Notes
        -----
        In Django's normal form rendering workflow, this method is called to
        process a value for display in a widget. However, for a Django
        :class:`django.forms.fields.MultiValueField`, the method is not called
        for `sub fields`.

        However, :meth:`calingen.forms.fields.plugin.PluginField.prepare_value`
        calls this method.
        """
        return ", ".join(value)

    def to_python(self, value):
        """Merge a comma-seperated list of strings to a Python list."""
        if not value:
            return []

        return [item.strip() for item in value.split(",")]


class PluginField(MultiValueField):
    """Custom Django field can handle the JSON object related to plugins."""

    widget = PluginWidget

    def __init__(self, *args, choices=(), **kwargs):
        self.choices = choices

        fields = (MultipleChoiceField(), CalingenListField())

        super().__init__(fields=fields, *args, **kwargs)

        self.fields[0].choices = self.choices
        self.widget.update_available_plugins(self.choices)

    def prepare_value(self, value):
        """Prepare the value / values for display."""
        prepared_list_field = self.fields[1].prepare_value(value["unavailable"])
        value["unavailable"] = prepared_list_field

        return super().prepare_value(value)

    def compress(self, data_list):
        """Compress the values of multiple fields into one object for the ORM layer.

        Notes
        -----
        See the corresponding :meth:`calingen.forms.widgets.PluginWidget.decompress`
        method.
        """
        if data_list:
            result = {}
            result["active"] = data_list[0]
            result["unavailable"] = data_list[1]
            return result
        return None
