# SPDX-License-Identifier: MIT

"""Provide Form implementations with generic functionality."""

# Django imports
from django.forms import Form


class RequestEnabledForm(Form):
    """Form class with the ``request`` object available."""

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
