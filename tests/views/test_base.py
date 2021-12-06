# SPDX-License-Identifier: MIT

"""Provide tests for calingen.models.profile."""

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
        self.user = User.objects.get(pk=5)
        self.client = Client()
        self.client.force_login(self.user)

        response = self.client.get(reverse("homepage"), follow=True)

        self.assertRedirects(response, reverse("profile-add"))

    def test_profile_available(self):
        self.user = User.objects.get(pk=2)
        self.profile = Profile.objects.get(owner=self.user)
        self.client = Client()
        self.client.force_login(self.user)

        response = self.client.get(reverse("homepage"), follow=True)

        self.assertRedirects(response, reverse("profile", args=[self.profile.id]))
