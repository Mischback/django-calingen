# SPDX-License-Identifier: MIT

"""Provide tests for calingen.checks."""

# Python imports
# import os
# import subprocess  # nosec: required for TeX compilation
# import tempfile
from unittest import mock, skip  # noqa: F401

# Django imports
from django.test import modify_settings, override_settings, tag  # noqa: F401

# app imports
from calingen.contrib.layouts.simple_event_list.simple_event_list import SimpleEventList
from calingen.contrib.layouts.year_by_week.year_by_week import YearByWeek

# local imports
from .util.testcases import CalingenTeXLayoutCompilationTestCase


class CalingenContribLayoutCompilationTest(CalingenTeXLayoutCompilationTestCase):
    @modify_settings(
        INSTALLED_APPS={"append": "calingen.contrib.layouts.simple_event_list"}
    )
    def test_simple_event_list_empty(self):
        # Arrange
        test_context = {}
        test_context["target_year"] = 2021
        test_context["layout_configuration"] = None

        test_filename = "simple_event_list_empty.tex"

        rendered_tex = SimpleEventList.render(test_context)

        # Act
        return_value = self.write_tex_to_tmp(rendered_tex, test_filename)

        # Assert
        self.assertTrue(return_value)

    @modify_settings(
        INSTALLED_APPS={"append": "calingen.contrib.layouts.simple_event_list"}
    )
    def test_simple_event_list_with_events(self):
        # Arrange
        test_target_year = 2021
        test_context = {}
        test_context["entries"] = self.get_entries(test_target_year)
        test_context["target_year"] = test_target_year
        test_context["layout_configuration"] = None

        test_filename = "simple_event_list_full.tex"

        rendered_tex = SimpleEventList.render(test_context)

        # Act
        return_value = self.write_tex_to_tmp(rendered_tex, test_filename)

        # Assert
        self.assertTrue(return_value)

    @modify_settings(INSTALLED_APPS={"append": "calingen.contrib.layouts.year_by_week"})
    def test_year_by_week_empty(self):
        # Arrange
        test_context = {}
        test_context["target_year"] = 2021
        test_context["layout_configuration"] = None

        test_filename = "year_by_week_empty.tex"

        rendered_tex = YearByWeek.render(test_context)

        # Act
        return_value = self.write_tex_to_tmp(rendered_tex, test_filename)

        # Assert
        self.assertTrue(return_value)

    @modify_settings(INSTALLED_APPS={"append": "calingen.contrib.layouts.year_by_week"})
    def test_year_by_week_with_events(self):
        # Arrange
        test_target_year = 2021
        test_context = {}
        test_context["entries"] = self.get_entries(test_target_year)
        test_context["target_year"] = test_target_year
        test_context["layout_configuration"] = None

        test_filename = "year_by_week_full.tex"

        rendered_tex = YearByWeek.render(test_context)

        # Act
        return_value = self.write_tex_to_tmp(rendered_tex, test_filename)

        # Assert
        self.assertTrue(return_value)
