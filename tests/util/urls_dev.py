# SPDX-License-Identifier: MIT

"""Provides a minimum url configuration to run the app with Django project."""

# Django imports
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
]

urlpatterns += i18n_patterns(
    path("calingen/", include("calingen.urls")), prefix_default_language=False
)

try:
    # django-debug-toolbar is only required during development
    # external imports
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

except ModuleNotFoundError:
    # This catches the ModuleNotFoundError during testing
    # django-debug-toolbar is just a development requirement
    pass
