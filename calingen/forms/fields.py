# SPDX-License-Identifier: MIT

"""Provide app-specific form fields."""


# Django imports
from django.core.exceptions import ValidationError
from django.forms.fields import (
    CharField,
    MultipleChoiceField,
    MultiValueField,
    SplitDateTimeField,
)

# app imports
from calingen.forms.widgets import PluginWidget


class SplitDateTimeOptionalField(SplitDateTimeField):
    """An app-specific implementation of Django's ``SplitDateTimeField``.

    While Django's default implementation of
    :class:`django.forms.fields.SplitDateTimeField` requires a `valid` value for
    both, ``date`` and ``time``, `calingen` will be happy with just a date and
    then assume that the ``time`` is ``"00:00:00"``.
    """

    def clean(self, value):
        """Catch validation errors of the ``time`` part and provide a fallback.

        Parameters
        ----------
        value : any
            The value to be cleaned.
            As this is derived from a :class:`django.forms.fields.MultiValueField`,
            the ``value`` will actually be a tuple, containing the values for
            the ``date`` and the ``time`` part.
            This method just provides a fallback for the ``time`` part and then
            uses ``super().clean(value)`` to chain further validation/cleaning
            steps.
        """
        try:
            self.fields[1].to_python(value[1])
        except ValidationError:
            value[1] = "00:00:00"

        return super().clean(value)


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

        However, :meth:`calingen.forms.fields.PluginField.prepare_value`
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
