# SPDX-License-Identifier: MIT

"""Provide tests for calingen.views.profile."""

# Python imports
from unittest import mock, skip  # noqa: F401

# Django imports
from django.contrib.auth.models import User
from django.test import Client, override_settings, tag  # noqa: F401
from django.urls import reverse

# local imports
from ..util.testcases import CalingenORMTransactionTestCase


@tag("views", "profile", "ProfileCreateView")
class ProfileCreateViewTest(CalingenORMTransactionTestCase):
    # This is based on Django's TransactionTestCase to make
    # test_profile_already_exists work!
    # Problem is the method of resetting the database to a known state after
    # the tests. As the subject under test relies on the database's
    # IntegrityError, the default Django TestCase does not work.

    def test_profile_does_not_exist(self):
        # Arrange (set up test environment)
        self.user = User.objects.get(pk=5)
        self.client = Client()
        self.client.force_login(self.user)
        # Alice=1, Bob=2, Charly=3...
        expected_profile_id = 4

        # Act (actually perform what has to be done)
        response = self.client.post(reverse("calingen:profile-add"), follow=True)

        # Assert (verify the results)
        self.assertRedirects(
            response,
            reverse("calingen:profile", kwargs={"profile_id": expected_profile_id}),
        )

    def test_profile_already_exists(self):
        # Arrange (set up test environment)
        self.user = User.objects.get(pk=2)  # Alice!
        self.client = Client()
        self.client.force_login(self.user)
        # Alice=1, Bob=2, Charly=3...
        expected_profile_id = 1

        # Act (actually perform what has to be done)
        response = self.client.post(reverse("calingen:profile-add"), follow=True)

        # Assert (verify the results)
        self.assertRedirects(
            response,
            reverse("calingen:profile", kwargs={"profile_id": expected_profile_id}),
        )
