# SPDX-License-Identifier: MIT

"""Provide tests for calingen.views.base."""

# Python imports
from unittest import mock, skip  # noqa: F401

# Django imports
from django.contrib.auth.models import User
from django.test import Client, override_settings, tag  # noqa: F401
from django.urls import reverse

# app imports
from calingen.models.profile import Profile

# local imports
from ..util.testcases import CalingenORMTestCase


@tag("views", "base", "homepage")
class CalingenHomepageTest(CalingenORMTestCase):
    def test_profile_not_available(self):
        # Arrange (set up test environment)
        self.user = User.objects.get(pk=5)
        self.client = Client()
        self.client.force_login(self.user)

        # Act (actually perform what has to be done)
        response = self.client.get(reverse("calingen:homepage"), follow=True)

        # Assert (verify the results)
        self.assertRedirects(response, reverse("calingen:profile-add"))

    def test_profile_available(self):
        # Arrange (set up test environment)
        self.user = User.objects.get(pk=2)
        self.profile = Profile.objects.get(owner=self.user)
        self.client = Client()
        self.client.force_login(self.user)

        # Act (actually perform what has to be done)
        response = self.client.get(reverse("calingen:homepage"), follow=True)

        # Assert (verify the results)
        self.assertRedirects(
            response, reverse("calingen:profile", args=[self.profile.id])
        )
