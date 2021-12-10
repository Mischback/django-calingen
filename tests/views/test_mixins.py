# SPDX-License-Identifier: MIT

"""Provide tests for calingen.views.mixins."""

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
    AllCalenderEntriesMixin,
    ProfileIDMixin,
    RestrictToUserMixin,
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


class RestrictToUserMixinAppliedView(RestrictToUserMixin, QuerySetView):
    """Combines the app's mixin with a dummy CBV."""

    model = None


class UserProfileIDMixinAppliedView(ProfileIDMixin, ContextMixin, TestTemplateView):
    pass


class AllCalenderEntriesMixinAppliedView(
    AllCalenderEntriesMixin, ContextMixin, TestTemplateView
):
    pass


@tag("views", "mixins", "RestrictToUserMixin")
class RestrictToUserMixinTest(CalingenTestCase):

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


@tag("views", "mixins", "ProfileIDMixin")
class ProfileIDMixinTest(CalingenTestCase):

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


@tag("views", "mixins", "AllCalenderEntriesMixin")
class AllCalenderEntriesMixinTest(CalingenTestCase):

    factory = RequestFactory()

    @mock.patch("calingen.views.mixins.Event")
    @mock.patch("calingen.views.mixins.Profile")
    def test_mixin_resolves_profile_and_events(self, mock_profile, mock_event):
        # Arrange (set up test environment)
        mock_profile_manager = mock.PropertyMock()
        mock_profile.calingen_manager = mock_profile_manager
        mock_event_manager = mock.PropertyMock()
        mock_event.calingen_manager = mock_event_manager
        test_target_year = 2021
        cbv = AllCalenderEntriesMixinAppliedView
        request = self.factory.get("/rand")
        request.user = "foo"
        view = cbv.as_view()

        # Act (actually perform what has to be done)
        response = view(request, target_year=test_target_year)

        # Assert (verify the results)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_profile_manager.get_profile.called)
        self.assertTrue(mock_event_manager.get_calender_entry_list.called)
