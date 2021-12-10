# SPDX-License-Identifier: MIT

"""Provide View implementations with generic functionality."""


# Django imports
from django.views.generic.edit import FormView


class RequestEnabledFormView(FormView):
    """Basically just a :class:`~django.views.generic.edit.FormView` that makes the ``request`` available on the form."""

    def get_form_kwargs(self, *args, **kwargs):
        """Pass the ``request`` object to the form.

        The ``request`` is passed to the form, so that the
        :meth:`~calingen.forms.tex.TeXLayoutSelectionForm.save_selection` can
        actually save the selected layout to the user's ``Session`` object.
        """
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs["request"] = self.request
        return kwargs
