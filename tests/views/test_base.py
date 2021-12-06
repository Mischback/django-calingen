# SPDX-License-Identifier: MIT

"""Provide tests for calingen.models.profile."""

# Python imports
from unittest import mock, skip  # noqa: F401

# Django imports
from django.test import RequestFactory, override_settings, tag  # noqa: F401

# app imports
from calingen.views.base import homepage

# local imports
from ..util.testcases import CalingenTestCase


@tag("views", "base", "homepage")
class CalingenHomepageTest(CalingenTestCase):

    factory = RequestFactory()

    @mock.patch("calingen.views.base.redirect")
    @mock.patch("calingen.views.base.Profile")
    def test_profile_not_available(self, mock_profile, mock_redirect):
        # Arrange (set up test environment)
        mock_profile_manager = mock.PropertyMock()
        mock_profile_manager.get_profile.return_value = None
        mock_profile.calingen_manager = mock_profile_manager
        request = self.factory.get("/rand")
        request.user = "foo"
        view = homepage.__wrapped__

        # Act (actually perform what has to be done)
        response = view(request)  # noqa: F841

        # Assert (verify the results)
        self.assertTrue(mock_profile_manager.get_profile.called)
        self.assertTrue(mock_redirect.called)
        mock_redirect.assert_called_with("profile-add")

    @mock.patch("calingen.views.base.redirect")
    @mock.patch("calingen.views.base.Profile")
    def test_profile_available(self, mock_profile, mock_redirect):
        # Arrange (set up test environment)
        mock_profile_manager = mock.PropertyMock()
        mock_profile_manager.get_profile.return_value = mock.Mock()
        mock_profile.calingen_manager = mock_profile_manager
        request = self.factory.get("/rand")
        request.user = "foo"
        view = homepage.__wrapped__

        # Act (actually perform what has to be done)
        response = view(request)  # noqa: F841

        # Assert (verify the results)
        self.assertTrue(mock_profile_manager.get_profile.called)
        self.assertTrue(mock_redirect.called)
        mock_redirect.assert_called_with(
            "profile", profile_id=mock_profile_manager.get_profile.return_value.id
        )
