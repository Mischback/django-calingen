# SPDX-License-Identifier: MIT

"""App-specific implementations of :class:`django.forms.fields.Field`."""

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
    """App-specific implementation of Django's ``SplitDateTimeField``.

    While Django's default implementation of
    :class:`django.forms.fields.SplitDateTimeField` requires a `valid` value for
    both, ``date`` and ``time``, `calingen` will be happy with just a date and
    then assume that the ``time`` is ``"00:00"``.

    Warnings
    --------
    The field will accept an *empty value* for the ``time`` part, but will
    actually provide a default value of ``"00:00"`` on processing the form.

    This means, that the database will contain a :py:obj:`datetime.datetime`
    object with ``time``.
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
            if self.fields[1].to_python(value[1]) is None:
                value[1] = "00:00"
        except ValidationError:
            value[1] = "00:00"

        return super().clean(value)


class CalingenListField(CharField):
    """Misuse a ``CharField`` to handle a list of strings."""

    def prepare_value(self, value):
        """Create a comma-seperated list of strings from a Python list.

        Parameters
        ----------
        value : list

        Returns
        -------
        str
            The ``value`` :py:obj:`list` is split and provided as a
            :py:obj:`str` of comma-seperated values.

        Notes
        -----
        In Django's normal form rendering workflow, this method is called to
        process a value for display in a widget. However, for a Django
        :class:`django.forms.fields.MultiValueField`, the method is not called
        for `sub fields`.

        As this field is specifically intended to work with
        :class:`~calingen.forms.fields.PluginField`,
        :meth:`its prepare_value() <calingen.forms.fields.PluginField.prepare_value>`
        method calls this method.
        """
        return ", ".join(value)  # pragma: nocover

    def to_python(self, value):
        """Convert a comma-seperated list of values to a Python list.

        Parameters
        ----------
        value : str

        Returns
        -------
        list
            The ``value`` :py:obj:`str` is split and converted in an actual
            Python :py:obj:`list`.

        Notes
        -----
        While :meth:`~calingen.forms.fields.CalingenListField.prepare_value` has
        to be called specifically, this very method is called automatically
        during form processing.
        """
        if not value:
            return []

        return [item.strip() for item in value.split(",")]


class PluginField(MultiValueField):
    """Custom field to manage JSON objects related to plugins.

    :class:`calingen.models.profile.Profile` is used to manage the user's
    selection of :class:`~calingen.interfaces.plugin_api.EventProvider` plugins.

    :meth:`calingen.models.profile.Profile.event_provider` handles this
    internally and maintains a specific JSON schema (without formally defining
    it), tracking ``active`` and ``unavailable`` instances of
    :class:`~calingen.interfaces.plugin_api.EventProvider`.

    While the model stores this as a :class:`~django.db.models.JSONField`, this
    custom field is used to present it in a form context.

    Warnings
    --------
    Currently this is very tightly connected to the actual implementation in
    :meth:`calingen.models.profile.Profile.event_provider` and will work only
    with that model / field *out of the box*.

    Additionally, it will only work with
    :class:`calingen.forms.widgets.PluginWidget`, because this class's
    :meth:`~calingen.forms.fields.PluginField.compress` method needs a
    counterpart in the widget's
    :meth:`~calingen.forms.widgets.PluginWidget.decompress` method.

    Notes
    -----
    The implementation extends
    :class:`django.forms.fields.MultiValueField` and provides the ``active``
    plugins in a :class:`django.forms.fields.MultipleChoiceField` and tracks the
    ``unavailable`` plugins in a
    :class:`calingen.forms.fields.CalingenListField`.
    """

    widget = PluginWidget
    """Use :class:`~calingen.forms.widgets.PluginWidget` as the fields widget."""

    def __init__(self, *args, choices=(), **kwargs):
        self.choices = choices

        fields = (MultipleChoiceField(), CalingenListField())

        super().__init__(fields=fields, *args, **kwargs)

        self.fields[0].choices = self.choices
        self.widget.update_available_plugins(self.choices)

    def prepare_value(self, value):
        """Prepare the value / values for display.

        Parameters
        ----------
        value : dict
            ``value`` is actually a JSON object as fetched from
            :meth:`Profile.event_provider <calingen.models.profile.Profile.event_provider>`.

        Notes
        -----
        This method *splits* the ``value`` to be used by the widgets.

        Additionally it ensures, that
        :meth:`CalingenListField.prepare_value <calingen.forms.fields.CalingenListField.prepare_value>`
        is called to handle the ``unavailable`` plugins.
        """
        prepared_list_field = self.fields[1].prepare_value(value["unavailable"])
        value["unavailable"] = prepared_list_field

        return super().prepare_value(value)

    def compress(self, data_list):
        """Compress the values of multiple fields into one object for the ORM layer.

        Parameters
        ----------
        data_list : list
            A :py:obj:`list` of values as provided by the multiple widgets of
            :class:`~calingen.forms.widgets.PluginWidget`.

        Returns
        -------
        obj
            Converts the ``data_list`` back to a object, satisfying
            :meth:`Profile.event_provider's <calingen.models.profile.Profile.event_provider>`
            JSON scheme.

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
