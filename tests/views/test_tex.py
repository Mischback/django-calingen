# SPDX-License-Identifier: MIT

"""Provide tests for calingen.views.tex."""

# Python imports
from unittest import mock, skip  # noqa: F401

# Django imports
from django.contrib.auth.models import User
from django.test import Client, override_settings, tag  # noqa: F401
from django.urls import reverse

# app imports
from calingen.views.tex import TeXLayoutConfigurationView, TeXLayoutSelectionView

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
        response = self.client.post(reverse("tex-layout-selection"), follow=True)

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
        response = self.client.get(reverse("tex-layout-configuration"), follow=True)

        # Assert (verify the results)
        self.assertRedirects(response, reverse("tex-layout-selection"))
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
        response = self.client.get(reverse("tex-layout-configuration"), follow=True)

        # Assert (verify the results)
        self.assertRedirects(response, reverse("tex-layout-selection"))
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