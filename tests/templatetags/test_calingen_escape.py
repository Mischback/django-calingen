# SPDX-License-Identifier: MIT

"""Provide tests for calingen.templatetags.calingen_escape."""

# Python imports
from unittest import mock, skip  # noqa: F401

# Django imports
from django.test import override_settings, tag  # noqa: F401

# app imports
from calingen.templatetags.calingen_escape import escape_tex

# local imports
from ..util.testcases import CalingenTestCase


@tag("templatetags", "calingen_escape")
class CalingenChecksTest(CalingenTestCase):
    def test_escape_tex_empty(self):
        # Arrange (set up test environment)
        test_input = ""
        test_output = ""

        # Act (actually perform what has to be done)
        return_value = escape_tex(test_input)

        # Assert (verify the results)
        self.assertEqual(return_value, test_output)

    def test_escape_tex_ampersand(self):
        # Arrange (set up test environment)
        test_input = r"&"
        test_output = r"\&"

        # Act (actually perform what has to be done)
        return_value = escape_tex(test_input)

        # Assert (verify the results)
        self.assertEqual(return_value, test_output)

    def test_escape_tex_percent(self):
        # Arrange (set up test environment)
        test_input = r"%"
        test_output = r"\%"

        # Act (actually perform what has to be done)
        return_value = escape_tex(test_input)

        # Assert (verify the results)
        self.assertEqual(return_value, test_output)

    def test_escape_tex_dollar(self):
        # Arrange (set up test environment)
        test_input = r"$"
        test_output = r"\$"

        # Act (actually perform what has to be done)
        return_value = escape_tex(test_input)

        # Assert (verify the results)
        self.assertEqual(return_value, test_output)

    def test_escape_tex_hash(self):
        # Arrange (set up test environment)
        test_input = r"#"
        test_output = r"\#"

        # Act (actually perform what has to be done)
        return_value = escape_tex(test_input)

        # Assert (verify the results)
        self.assertEqual(return_value, test_output)

    def test_escape_tex_underscore(self):
        # Arrange (set up test environment)
        test_input = r"_"
        test_output = r"\_"

        # Act (actually perform what has to be done)
        return_value = escape_tex(test_input)

        # Assert (verify the results)
        self.assertEqual(return_value, test_output)

    def test_escape_tex_curly_left(self):
        # Arrange (set up test environment)
        test_input = r"{"
        test_output = r"\{"

        # Act (actually perform what has to be done)
        return_value = escape_tex(test_input)

        # Assert (verify the results)
        self.assertEqual(return_value, test_output)

    def test_escape_tex_curly_right(self):
        # Arrange (set up test environment)
        test_input = r"}"
        test_output = r"\}"

        # Act (actually perform what has to be done)
        return_value = escape_tex(test_input)

        # Assert (verify the results)
        self.assertEqual(return_value, test_output)

    def test_escape_tex_tilde(self):
        # Arrange (set up test environment)
        test_input = r"~"
        test_output = r"\texttt{\~{}}"

        # Act (actually perform what has to be done)
        return_value = escape_tex(test_input)

        # Assert (verify the results)
        self.assertEqual(return_value, test_output)

    def test_escape_tex_exp(self):
        # Arrange (set up test environment)
        test_input = r"^"
        test_output = r"\^{}"

        # Act (actually perform what has to be done)
        return_value = escape_tex(test_input)

        # Assert (verify the results)
        self.assertEqual(return_value, test_output)

    def test_escape_tex_backslash(self):
        # Arrange (set up test environment)
        test_input = r"\ "
        test_output = r"$\backslash$ "

        # Act (actually perform what has to be done)
        return_value = escape_tex(test_input)

        # Assert (verify the results)
        self.assertEqual(return_value, test_output)

    def test_escape_tex_full(self):
        # Arrange (set up test environment)
        test_input = r"& % $ # _ { } ~ ^ \ \today"
        test_output = (
            r"\& \% \$ \# \_ \{ \} \texttt{\~{}} \^{} $\backslash$ $\backslash$today"
        )

        # Act (actually perform what has to be done)
        return_value = escape_tex(test_input)

        # Assert (verify the results)
        self.assertEqual(return_value, test_output)
