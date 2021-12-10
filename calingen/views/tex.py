# SPDX-License-Identifier: MIT

"""Provide views in the context of TeX rendering and compilation."""

# Django imports
from django.urls import reverse_lazy

# app imports
from calingen.forms.tex import TeXLayoutSelectionForm
from calingen.views.generic import RequestEnabledFormView


class TeXLayoutSelectionView(RequestEnabledFormView):
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
