# SPDX-License-Identifier: MIT

"""Provide views in the context of TeX rendering and compilation."""

# Django imports
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

# app imports
from calingen.forms.tex import TeXLayoutSelectionForm


class TeXLayoutSelectionView(FormView):
    """Provide a list of availabe layouts.

    Warnings
    --------
    This view is not restricted to users with a
    :class:`Calingen Profile <calingen.models.profile.Profile>` and can be
    accessed by any user of the project.

    However, on actual generation and compilation of the output, a
    ``Profile`` is required.

    Notes
    -----
    This is just the view to show and process the
    :class:`calingen.forms.tex.TeXLayoutSelectionForm`.

    Relevant logic, that affects the actual creation, rendering and compilation
    of TeX-templates is provided in the corresponding
    :class:`~django.forms.Form` instance.
    """

    template_name = "calingen/tex_layout_selection.html"
    form_class = TeXLayoutSelectionForm
    success_url = reverse_lazy("homepage")

    def form_valid(self, form):
        """Trigger saving of the selected value in the user's ``Session``."""
        form.save_selection()
        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        """Pass the ``request`` object to the form.

        The ``request`` is passed to the form, so that the
        :meth:`~calingen.forms.tex.TeXLayoutSelectionForm.save_selection` can
        actually save the selected layout to the user's ``Session`` object.
        """
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs["request"] = self.request
        return kwargs
