# SPDX-License-Identifier: MIT

"""Provides Django form fields related to date and time processing."""

# Django imports
from django.core.exceptions import ValidationError
from django.forms.fields import SplitDateTimeField


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
