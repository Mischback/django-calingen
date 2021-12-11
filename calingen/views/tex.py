# SPDX-License-Identifier: MIT

"""Provide views in the context of TeX rendering and compilation."""

# Python imports
import logging
from io import StringIO

# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import FileResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.module_loading import import_string
from django.views.generic.base import ContextMixin, View

# app imports
from calingen.exceptions import CalingenException
from calingen.forms.tex import TeXLayoutSelectionForm
from calingen.views.generic import RequestEnabledFormView
from calingen.views.mixins import AllCalenderEntriesMixin, RestrictToUserMixin

logger = logging.getLogger(__name__)


class TeXGeneratorView(
    LoginRequiredMixin, RestrictToUserMixin, AllCalenderEntriesMixin, ContextMixin, View
):
    """Use the layout's ``render()`` method to generate valid TeX source."""

    def get(self, request, *args, **kwargs):
        """Just for Linting."""
        selected_layout = request.session.pop("selected_layout", None)
        if selected_layout is None:
            # This is most likely an edge case: The view is accessed with a
            # GET request without a selected layout stored in the user's session.
            # This could be caused by directly calling this view's url.
            # Just redirect to the layout selection.
            return redirect("tex-layout-selection")
        logger.debug(selected_layout)
        layout = import_string(selected_layout)

        layout_configuration = request.session.pop("layout_configuration", None)

        # FIXME: The target year must be provided elsewhere!
        #        Idea: Include it into TeXLayoutSelectionForm, store it in the
        #              session and retrieve it here!
        # TODO: Same technique can be used for the layout configuration!
        context = self.get_context_data(
            target_year=2022, layout_configuration=layout_configuration, **kwargs
        )
        logger.debug("context:")
        logger.debug(context)
        # FIXME: The following is just for debugging!
        context["ctx"] = context

        rendered = StringIO()
        rendered.write(layout.render(context))
        rendered.seek(0)
        response = FileResponse(
            rendered.read(), as_attachment=True, filename="foobar.txt"
        )

        return response


class TeXLayoutConfigurationView(LoginRequiredMixin, RequestEnabledFormView):
    """Show configuration form for the selected layout.

    Warnings
    --------
    This view is not restricted to users with a
    :class:`Calingen Profile <calingen.models.profile.Profile>` and can be
    accessed by any user of the project.

    However, on actual generation and compilation of the output, a
    ``Profile`` is required.

    Notes
    -----
    This is just the view to show and process the layout's implementation of
    :class:`calingen.forms.tex.TeXLayoutConfigurationForm`.
    """

    template_name = "calingen/tex_layout_configuration.html"
    success_url = reverse_lazy("tex-generator")

    class NoConfigurationFormException(CalingenException):
        """Raised if the selected layout does not have a ``configuration_form``."""

    class NoLayoutSelectedException(CalingenException):
        """Raised if there is no selected layout in the user's ``Session``."""

    def form_valid(self, form):
        """Trigger saving of the configuration values in the user's ``Session``."""
        form.save_configuration()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        """Handle a GET request to the view.

        While processing the request, it is determined if the selected
        implementation of :class:`calingen.interfaces.plugin_api.LayoutProvider`
        uses a custon ``configuration_form``.

        If no custom configuration is implemented by the layout, the request
        is redirected to the generator.

        Notes
        -----
        Determining the ``configuration_form`` is done implicitly while
        traversing the view's hierarchy during processing the request. Several
        methods are involved, but at some point
        :meth:`~calingen.views.tex.TeXLayoutConfigurationView.get_form_class` is
        called, which will raise an exceptions that is handled here.

        If there is not selected layout in the user's ``Session``, a redirect to
        the user's profile overview is performed.
        """
        try:
            return super().get(request, *args, **kwargs)
        except self.NoConfigurationFormException:
            # As no layout specific configuration form is required, directly
            # redirect to the tex generation.
            return redirect("tex-generator")
        except self.NoLayoutSelectedException:
            # This is most likely an edge case: The view is accessed with a
            # GET request without a selected layout stored in the user's session.
            # This could be caused by directly calling this view's url.
            # Just redirect to the layout selection.
            return redirect("tex-layout-selection")

    def get_form_class(self):
        """Provide the layout's configuration form.

        Notes
        -----
        Implementations of :class:`calingen.interfaces.plugin_api.LayoutProvider`
        may provide a class attribute ``configuration_form`` with a subclass of
        :class:`calingen.forms.tex.TeXLayoutConfigurationForm`.

        If ``configuration_form`` is omitted, a custom exception is raised, that
        will be handled in
        :meth:`~calingen.views.tex.TeXLayoutConfigurationView.get`.

        If there is no selected layout in the user's ``Session``, a different
        custom exception will cause a redirect to the user's profile overview.
        """
        selected_layout = self.request.session.get("selected_layout", None)
        if selected_layout is None:
            raise self.NoLayoutSelectedException()

        layout = import_string(selected_layout)
        if layout.configuration_form is None:
            raise self.NoConfigurationFormException()

        return layout.configuration_form


class TeXLayoutSelectionView(LoginRequiredMixin, RequestEnabledFormView):
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
    success_url = reverse_lazy("tex-layout-configuration")

    def form_valid(self, form):
        """Trigger saving of the selected value in the user's ``Session``."""
        form.save_selection()
        return super().form_valid(form)
