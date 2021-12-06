# SPDX-License-Identifier: MIT

"""Provide tests for calingen.models.profile."""

# Python imports
from unittest import mock, skip  # noqa: F401

# Django imports
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.test import RequestFactory, override_settings, tag  # noqa: F401
from django.views.generic import View

# app imports
from calingen.views.mixins import CalingenRestrictToUserMixin

# local imports
from ..util.testcases import CalingenTestCase


class QuerySetView(View):
    """Just a dummy CBV to test the app's mixins with database access."""

    def get(self, request, *args, **kwargs):
        objects = self.get_queryset()  # noqa: F841

        return HttpResponse()


class RestrictToUserMixinAppliedView(CalingenRestrictToUserMixin, QuerySetView):
    """Combines the app's mixin with a dummy CBV."""

    model = None


@tag("views", "mixins")
class CalingenRestrictToUserMixinTest(CalingenTestCase):

    factory = RequestFactory()

    def test_mixin_raises_error_on_missing_model(self):
        """The attribute `model` is required."""
        request = self.factory.get("/rand")
        request.user = "foo"
        view = RestrictToUserMixinAppliedView.as_view()

        with self.assertRaises(ImproperlyConfigured):
            response = view(request)  # noqa: F841

    def test_mixin_uses_stockings_manager_method(self):
        """The app-specific manager is correctly called."""
        cbv = RestrictToUserMixinAppliedView
        cbv.model = mock.MagicMock()

        request = self.factory.get("/rand")
        request.user = "foo"
        view = cbv.as_view()

        response = view(request)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            cbv.model.calingen_manager.get_queryset.return_value.filter_by_user.called
        )
        cbv.model.calingen_manager.get_queryset.return_value.filter_by_user.assert_called_with(
            request.user
        )
