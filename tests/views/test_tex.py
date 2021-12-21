# SPDX-License-Identifier: MIT

"""Provide tests for calingen.views.tex."""

# Python imports
from unittest import mock, skip  # noqa: F401

# Django imports
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.test import Client, override_settings, tag  # noqa: F401
from django.urls import reverse

# app imports
from calingen.views.tex import (
    TeXCompilerView,
    TeXLayoutConfigurationView,
    TeXLayoutSelectionView,
)

# local imports
from ..util.testcases import CalingenORMTestCase


@tag("views", "tex", "TeXLayoutSelectionView")
class TeXLayoutSelectionViewTest(CalingenORMTestCase):
    def test_form_must_contain_data(self):
        # Arrange (set up test environment)
        self.user = User.objects.get(pk=2)
        self.client = Client()
        self.client.force_login(self.user)

        # Act (actually perform what has to be done)
        response = self.client.post(
            reverse("calingen:tex-layout-selection"), follow=True
        )

        # Assert (verify the results)
        # The actual verification, that an empty POST don't proceed to the next
        # step is done by checking the used template!
        # Works ok.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "calingen/tex_layout_selection.html")

    @mock.patch("calingen.views.tex.super")
    def test_form_valid(self, mock_super):
        # Arrange
        test_form = mock.MagicMock()
        cbv = TeXLayoutSelectionView()

        # Act
        cbv.form_valid(test_form)

        # Assert
        test_form.save_selection.assert_called_once()
        mock_super.return_value.form_valid.assert_called_once()


@tag("views", "tex", "TeXLayoutConfigurationView")
class TeXLayoutConfigurationViewTest(CalingenORMTestCase):
    @mock.patch(
        "calingen.views.tex.TeXLayoutConfigurationView.get_form_class",
        side_effect=TeXLayoutConfigurationView.NoLayoutSelectedException(),
    )
    def test_error_if_no_layout_is_selected(self, mock_get_form_class):
        # Arrange (set up test environment)
        self.user = User.objects.get(pk=2)
        self.client = Client()
        self.client.force_login(self.user)

        # Act (actually perform what has to be done)
        response = self.client.get(
            reverse("calingen:tex-layout-configuration"), follow=True
        )

        # Assert (verify the results)
        self.assertRedirects(response, reverse("calingen:tex-layout-selection"))
        mock_get_form_class.assert_called_once()

    @mock.patch(
        "calingen.views.tex.TeXLayoutConfigurationView.get_form_class",
        side_effect=TeXLayoutConfigurationView.NoConfigurationFormException(),
    )
    def test_error_if_no_configuration_is_required(self, mock_get_form_class):
        # Arrange (set up test environment)
        self.user = User.objects.get(pk=2)
        self.client = Client()
        self.client.force_login(self.user)

        # Act (actually perform what has to be done)
        response = self.client.get(
            reverse("calingen:tex-layout-configuration"), follow=True
        )

        # Assert (verify the results)
        self.assertRedirects(response, reverse("calingen:tex-layout-selection"))
        mock_get_form_class.assert_called_once()

    @mock.patch("calingen.views.tex.super")
    def test_form_valid(self, mock_super):
        # Arrange
        test_form = mock.MagicMock()
        cbv = TeXLayoutConfigurationView()

        # Act
        cbv.form_valid(test_form)

        # Assert
        test_form.save_configuration.assert_called_once()
        mock_super.return_value.form_valid.assert_called_once()

    def test_get_form_class_no_selection(self):
        # Arrange
        test_request = mock.MagicMock()
        test_request.session.get.return_value = None
        cbv = TeXLayoutConfigurationView()
        cbv.request = test_request

        # Act
        # Assert
        with self.assertRaises(TeXLayoutConfigurationView.NoLayoutSelectedException):
            cbv.get_form_class()

    @mock.patch("calingen.views.tex.import_string")
    def test_get_form_class_no_form(self, mock_import_string):
        # Arrange
        test_request = mock.MagicMock()
        test_request.session.get.return_value = "foo.bar"
        test_layout = mock.MagicMock()
        test_layout.configuration_form = None
        mock_import_string.return_value = test_layout
        cbv = TeXLayoutConfigurationView()
        cbv.request = test_request

        # Act
        # Assert
        with self.assertRaises(TeXLayoutConfigurationView.NoConfigurationFormException):
            cbv.get_form_class()

    @mock.patch("calingen.views.tex.import_string")
    def test_get_form_class_return_form(self, mock_import_string):
        # Arrange
        test_request = mock.MagicMock()
        test_request.session.get.return_value = "foo.bar"
        test_layout_form = mock.MagicMock()
        test_layout = mock.MagicMock()
        test_layout.configuration_form = test_layout_form
        mock_import_string.return_value = test_layout
        cbv = TeXLayoutConfigurationView()
        cbv.request = test_request

        # Act
        return_value = cbv.get_form_class()

        # Assert
        self.assertEqual(return_value, test_layout_form)


@tag("views", "tex", "TeXCompilerView")
class TeXCompilerViewTest(CalingenORMTestCase):
    @mock.patch(
        "calingen.views.tex.TeXCompilerView._get_layout",
        side_effect=TeXCompilerView.NoLayoutSelectedException(),
    )
    def test_error_if_no_layout_is_selected(self, mock_get_layout):
        # Arrange (set up test environment)
        self.user = User.objects.get(pk=2)
        self.client = Client()
        self.client.force_login(self.user)

        # Act (actually perform what has to be done)
        response = self.client.get(reverse("calingen:tex-compiler"), follow=True)

        # Assert (verify the results)
        self.assertRedirects(response, reverse("calingen:tex-layout-selection"))
        mock_get_layout.assert_called_once()

    @mock.patch("calingen.views.tex.import_string")
    def test_get_layout_return_imported_layout(self, mock_import_string):
        # Arrange
        test_request = mock.MagicMock()
        test_request.session.pop.return_value = "foo.bar"
        test_layout = mock.MagicMock()
        mock_import_string.return_value = test_layout
        cbv = TeXCompilerView()
        cbv.request = test_request

        # Act
        return_value = cbv._get_layout()

        # Assert
        self.assertEqual(return_value, test_layout)

    @mock.patch("calingen.views.tex.TeXCompilerView.get_context_data")
    def test_prepare_context(self, mock_get_context_data):
        # Arrange
        test_request = mock.MagicMock()
        test_request.session.pop.return_value = "foo"
        mock_kwargs = mock.MagicMock()
        cbv = TeXCompilerView()
        cbv.request = test_request

        # Act
        return_value = cbv._prepare_context()  # noqa: F841

        # Assert
        # test_form.save_configuration.assert_called_once()
        mock_get_context_data.assert_called_once()
        mock_get_context_data.assert_called_once_with(
            target_year="foo", layout_configuration="foo", **mock_kwargs
        )

    @mock.patch("calingen.views.tex.import_string")
    @mock.patch("calingen.views.tex.TeXCompilerView._prepare_context")
    @mock.patch("calingen.views.tex.TeXCompilerView._get_layout")
    def test_compilation(
        self, mock_get_layout, mock_prepare_context, mock_import_string
    ):
        # Arrange (set up test environment)
        mock_compiler = mock.MagicMock()
        mock_compiler.get_response.return_value = HttpResponse("foo")
        mock_layout = mock.MagicMock()
        mock_get_layout.return_value = mock_layout
        mock_import_string.return_value = mock_compiler
        self.user = User.objects.get(pk=2)
        self.client = Client()
        self.client.force_login(self.user)

        # Act (actually perform what has to be done)
        response = self.client.get(reverse("calingen:tex-compiler"), follow=True)

        # Assert (verify the results)
        self.assertContains(response, "foo")
        mock_get_layout.assert_called_once()
        mock_prepare_context.assert_called_once()
        mock_layout.render.assert_called_once()
        mock_layout.render.assert_called_once_with(mock_prepare_context.return_value)
        mock_compiler.get_response.assert_called_once()
