# SPDX-License-Identifier: MIT

"""Provide views in the context of TeX rendering and compilation."""

# Django imports
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

# app imports
from calingen.forms.tex import TeXLayoutSelectionForm


class TeXLayoutSelectionView(FormView):
    """Provide a list of availabe layouts.

    This is just the view to show and process the
    :class:`calingen.forms.tex.TeXLayoutSelectionForm`.

    Notes
    -----
    This view is not restricted to users with a
    :class:`Calingen Profile <calingen.models.profile.Profile>` and can be
    accessed by any user of the project.

    However, on actual generation and compilation of the output, a
    ``Profile`` is required.
    """

    template_name = "calingen/tex_layout_selection.html"
    form_class = TeXLayoutSelectionForm
    success_url = reverse_lazy("homepage")
