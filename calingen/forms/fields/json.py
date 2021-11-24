# SPDX-License-Identifier: MIT

"""Provides Django form fields related to JSON model fields."""

# Python imports
import logging

# Django imports
from django.forms.fields import MultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple

logger = logging.getLogger(__name__)


class JSONDataMultipleChoice(MultipleChoiceField):
    """Provide a MultipleChoiceField which translates to a JSON object.

    Notes
    -----
    The default ``FormField`` of :class:`django.db.models.JSONField` is a
    :class:`django.forms.fields.JSONField`, which uses a ``<textarea>`` as its
    input element.

    This field extends :class:`django.forms.fields.MultipleChoiceField` and
    enables the parsing of JSON values **from** the ORM layer
    (:meth:`~calingen.forms.fields.JSONDataMultipleChoice.prepare_value`) and
    **to** the ORM layer
    (:meth:`~calingen.forms.fields.JSONDataMultipleChoice.to_python`).

    Additionally, the input element is switched to
    :class:`~django.forms.widgets.CheckboxSelectMultiple`.
    """

    widget = CheckboxSelectMultiple

    def prepare_value(self, value):
        """Prepare the ORM representation for rendering in the widget.

        Parameters
        ----------
        value :
            ORM representation of the actual field (a pythonic JSON object).

        Returns
        -------
        list
            A list of strings, corresponding to the input JSON object's keys.
        """
        # value is a pythonic representation of a JSON object with a known
        # structure
        parsed_value = []

        for plugin in value:
            if plugin not in [available[0] for available in self.choices]:
                logger.warn("{} is not available in self.choices".format(plugin))

            # This basically works, but does not handle the case, that a value
            # is present in ORM that points to a plugin, that is not longer
            # available.
            # Possible solutions:
            # 1) ignore this:
            #    when the form (containing this field) is saved, the
            #    corresponding entry is gone, as it is lost
            # 2) inform the user: possibly Django's messaging framework could
            #    be used. This would be another (implicit) dependency, which
            #    might not be desirable.
            # For now, just put a logging message in place.
            # See issue #11
            parsed_value.append(plugin)

        return parsed_value

    def to_python(self, value):
        """Convert widget input for ORM layer.

        Parameters
        ----------
        value :
            Expected is a list of strings as returned by the
            CheckboxSelectMultiple widget.

        Returns
        -------
        dict
            A pythonic JSON object of the following structure:
            ``{ [item of value as string]: True }``
        """
        # re-use the original to_python() method to ensure that value is a list
        # of strings
        value = super().to_python(value)

        # bulid the pythonic representation of a JSON object
        data = {}
        for item in value:
            data[item] = True

        return data
