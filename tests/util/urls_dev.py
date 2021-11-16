# SPDX-License-Identifier: MIT

"""Provides a minimum url configuration to run the app with Django project."""

# Django imports
from django.conf.urls import include, url  # noqa: F401
from django.contrib import admin

urlpatterns = [
    url(r"^admin/", admin.site.urls),
]
