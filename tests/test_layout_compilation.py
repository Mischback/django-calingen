# SPDX-License-Identifier: MIT

"""Provide tests for calingen.checks."""

# Python imports
from unittest import mock, skip  # noqa: F401

# Django imports
from django.test import override_settings, tag  # noqa: F401

# local imports
from .util.testcases import CalingenTeXLayoutCompilationTestCase


class CalingenContribLayoutCompilationTest(CalingenTeXLayoutCompilationTestCase):
    def test_foo(self):
        raise NotImplementedError("To be done!")
