# SPDX-License-Identifier: MIT

"""Provide tests for calingen.views.tex."""

# Python imports
from unittest import mock, skip  # noqa: F401

# Django imports
from django.contrib.auth.models import User
from django.test import Client, override_settings, tag  # noqa: F401
from django.urls import reverse

# local imports
from ..util.testcases import CalingenORMTransactionTestCase


@tag("views", "tex", "TeXLayoutSelectionView")
class TeXLayoutSelectionViewTest(CalingenORMTransactionTestCase):
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
