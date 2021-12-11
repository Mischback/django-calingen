# SPDX-License-Identifier: MIT

"""Provide Form implementations with generic functionality."""

# Django imports
from django.forms import Form


class RequestEnabledForm(Form):
    """Form class with the ``request`` object available.

    Notes
    -----
    This form implementation is intended to be used together with
    :class:`calingen.views.generic.RequestEnabledFormView`. In fact, an actual
    form will subclass this form and use a view that is a subclass of
    :class:`~calingen.views.generic.RequestEnabledFormView`.
    """

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
