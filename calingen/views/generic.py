# SPDX-License-Identifier: MIT

"""View implementations with generic functionality."""


# Django imports
from django.views.generic.edit import FormView


class RequestEnabledFormView(FormView):
    """Basically just a :class:`~django.views.generic.edit.FormView` that makes the ``request`` available on the form.

    Notes
    -----
    This view implementation is intended to be used together with
    :class:`calingen.forms.generic.RequestEnabledForm`. In fact, an actual view
    will subclass this view and use a form that is a subclass of
    :class:`~calingen.forms.generic.RequestEnabledForm`.
    """

    def get_form_kwargs(self, *args, **kwargs):
        """Add the ``request`` object to the form during initialization."""
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs["request"] = self.request
        return kwargs
