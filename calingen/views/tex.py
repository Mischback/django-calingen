# SPDX-License-Identifier: MIT

"""Provide views in the context of TeX rendering and compilation."""

# Python imports
from datetime import date

# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.module_loading import import_string
from django.views.generic.base import ContextMixin, View

# app imports
from calingen.exceptions import CalingenException
from calingen.forms.tex import TeXLayoutSelectionForm
from calingen.views.generic import RequestEnabledFormView
from calingen.views.mixins import AllCalenderEntriesMixin, RestrictToUserMixin


class TeXGeneratorView(
    LoginRequiredMixin, RestrictToUserMixin, AllCalenderEntriesMixin, ContextMixin, View
):
    """Use the layout's ``render()`` method to generate valid TeX source."""

    class NoLayoutSelectedException(CalingenException):
        """Raised if there is no selected layout in the user's ``Session``."""

    def get(self, request, *args, **kwargs):
        """Trigger rendering of the selected layout and return the result.

        Notes
        -----
        The ``context`` that is passed to the layout's ``render()`` method
        contains the following ``keys``:

        - ``target_year``: The year to create the TeX layout for.
        - ``layout_configuration``: If the layout provides a custom
          implementation of :class:`calingen.forms.tex.TeXLayoutConfigurationForm`,
          the fetched values will be provided here.
        - ``entries``: All calender entries of the user's profile, resolved to
          the ``target_year``, provided as a
          :class:`calingen.interfaces.data_exchange.CalenderEntryList` object.

        If there is no selected layout in the user's ``Session``, a redirect to
        :class:`calingen.views.tex.TeXLayoutSelectionView` is performed.
        """
        try:
            self.layout = self._get_layout()
        except self.NoLayoutSelectedException:
            return redirect("tex-layout-selection")

        self.render_context = self._prepare_context(*args, **kwargs)

        return HttpResponse(self.layout.render(self.render_context))

    def _get_layout(self):
        selected_layout = self.request.session.pop("selected_layout", None)
        if selected_layout is None:
            # This is most likely an edge case: The view is accessed with a
            # GET request without a selected layout stored in the user's session.
            # This could be caused by directly calling this view's url.
            # Just redirect to the layout selection.
            raise self.NoLayoutSelectedException()

        return import_string(selected_layout)

    def _prepare_context(self, *args, **kwargs):
        target_year = self.request.session.pop("target_year", date.today().year)
        layout_configuration = self.request.session.pop("layout_configuration", None)

        return self.get_context_data(
            target_year=target_year, layout_configuration=layout_configuration, **kwargs
        )


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

        If there is no selected layout in the user's ``Session``, a redirect to
        :class:`calingen.views.tex.TeXLayoutSelectionView` is performed.
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
