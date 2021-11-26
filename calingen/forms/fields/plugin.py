# SPDX-License-Identifier: MIT


# Python imports
import logging

# Django imports
from django.forms.fields import JSONField, MultipleChoiceField, MultiValueField

# app imports
from calingen.forms.widgets import PluginWidget

logger = logging.getLogger(__name__)


class CalingenMultipleChoiceField(MultipleChoiceField):
    def __init__(self, *args, choices=(), **kwargs):
        logger.debug("running CalingenMultipleChoiceField.__init__()")

        super().__init__(*args, **kwargs)


class CalingenJSONField(JSONField):
    pass


class PluginField(MultiValueField):

    widget = PluginWidget

    def __init__(self, *args, choices=(), **kwargs):
        logger.debug("running PluginField.__init__()")

        fields = (CalingenMultipleChoiceField(choices=choices), CalingenJSONField())

        super().__init__(fields=fields, *args, **kwargs)

        self.widget.update_available_plugins(choices)
