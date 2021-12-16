# SPDX-License-Identifier: MIT

"""Provide tests for calingen.checks."""

# Python imports
import os
import subprocess  # nosec: required for TeX compilation
import tempfile
from unittest import mock, skip  # noqa: F401

# Django imports
from django.test import modify_settings, override_settings, tag  # noqa: F401

# app imports
from calingen.contrib.layouts.simple_event_list.simple_event_list import SimpleEventList

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

        test_filebasename = "foo"

        rendered_tex = SimpleEventList.render(test_context)

        # Act
        with tempfile.TemporaryDirectory() as tempdir:
            # determine expected filenames
            test_input_filename = os.path.join(tempdir, test_filebasename + ".tex")
            test_output_filename = os.path.join(tempdir, test_filebasename + ".pdf")

            with open(test_input_filename, "x", encoding="utf-8") as f:
                f.write(rendered_tex)

            args = [
                "lualatex",
                "--interaction=batchmode",
                "--output-directory={}".format(tempdir),
                test_input_filename,
            ]

            try:
                subprocess.check_call(args)  # nosec: Required for TeX compilation

            except subprocess.CalledProcessError as err:
                print("Handle this Error!")
                raise err

            # Assert
            self.assertTrue(os.path.exists(test_output_filename))
