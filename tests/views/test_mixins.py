# SPDX-License-Identifier: MIT

"""Provide tests for calingen.models.profile."""

# Python imports
from unittest import mock, skip  # noqa: F401

# Django imports
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.test import RequestFactory, override_settings, tag  # noqa: F401
from django.views.generic import View
from django.views.generic.base import ContextMixin

# app imports
from calingen.views.mixins import (
    CalingenRestrictToUserMixin,
    CalingenUserProfileIDMixin,
)

# local imports
from ..util.testcases import CalingenTestCase


class QuerySetView(View):
    """Just a dummy CBV to test the app's mixins with database access."""

    def get(self, request, *args, **kwargs):
        objects = self.get_queryset()  # noqa: F841

        return HttpResponse()


class TestTemplateView(View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)  # noqa: F841
        return HttpResponse()


class RestrictToUserMixinAppliedView(CalingenRestrictToUserMixin, QuerySetView):
    """Combines the app's mixin with a dummy CBV."""

    model = None


class UserProfileIDMixinAppliedView(
    CalingenUserProfileIDMixin, ContextMixin, TestTemplateView
):
    pass


@tag("views", "mixins", "CalingenRestrictToUserMixin")
class CalingenRestrictToUserMixinTest(CalingenTestCase):

    factory = RequestFactory()

    def test_mixin_raises_error_on_missing_model(self):
        """The attribute `model` is required."""
        # Arrange (set up test environment)
        request = self.factory.get("/rand")
        request.user = "foo"
        view = RestrictToUserMixinAppliedView.as_view()

        # Act (actually perform what has to be done)
        # Assert (verify the results))
        with self.assertRaises(ImproperlyConfigured):
            response = view(request)  # noqa: F841

    def test_mixin_uses_stockings_manager_method(self):
        """The app-specific manager is correctly called."""
        # Arrange (set up test environment)
        cbv = RestrictToUserMixinAppliedView
        cbv.model = mock.MagicMock()
        request = self.factory.get("/rand")
        request.user = "foo"
        view = cbv.as_view()

        # Act (actually perform what has to be done)
        response = view(request)

        # Assert (verify the results))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            cbv.model.calingen_manager.get_queryset.return_value.filter_by_user.called
        )
        cbv.model.calingen_manager.get_queryset.return_value.filter_by_user.assert_called_with(
            request.user
        )


@tag("views", "mixins", "CalingenUserProfileIDMixin")
class CalingenUserProfileIDMixinTest(CalingenTestCase):

    factory = RequestFactory()

    @mock.patch("calingen.views.mixins.Profile")
    def test_mixin_tries_to_determine_user_profile(self, mock_profile):
        # Arrange (set up test environment)
        mock_profile_manager = mock.PropertyMock()
        mock_profile.calingen_manager = mock_profile_manager
        cbv = UserProfileIDMixinAppliedView
        request = self.factory.get("/rand")
        request.user = "foo"
        view = cbv.as_view()

        # Act (actually perform what has to be done)
        response = view(request)

        # Assert (verify the results))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_profile_manager.get_profile.called)
