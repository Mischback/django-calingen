# SPDX-License-Identifier: MIT

"""Provide tests for calingen.templatetags.calingen_tex."""

# Python imports
from unittest import mock, skip  # noqa: F401

# Django imports
from django.test import override_settings, tag  # noqa: F401

# app imports
from calingen.templatetags.calingen_tex import escape_tex

# local imports
from ..util.testcases import CalingenTestCase


@tag("templatetags", "calingen_tex")
class CalingenChecksTest(CalingenTestCase):
    def test_escape_tex_empty(self):
        # Arrange (set up test environment)
        input = ""
        output = ""

        # Act (actually perform what has to be done)
        return_value = escape_tex(input)

        # Assert (verify the results)
        self.assertEqual(return_value, output)

    def test_escape_tex_ampersand(self):
        # Arrange (set up test environment)
        input = r"&"
        output = r"\&"

        # Act (actually perform what has to be done)
        return_value = escape_tex(input)

        # Assert (verify the results)
        self.assertEqual(return_value, output)

    def test_escape_tex_percent(self):
        # Arrange (set up test environment)
        input = r"%"
        output = r"\%"

        # Act (actually perform what has to be done)
        return_value = escape_tex(input)

        # Assert (verify the results)
        self.assertEqual(return_value, output)

    def test_escape_tex_dollar(self):
        # Arrange (set up test environment)
        input = r"$"
        output = r"\$"

        # Act (actually perform what has to be done)
        return_value = escape_tex(input)

        # Assert (verify the results)
        self.assertEqual(return_value, output)

    def test_escape_tex_hash(self):
        # Arrange (set up test environment)
        input = r"#"
        output = r"\#"

        # Act (actually perform what has to be done)
        return_value = escape_tex(input)

        # Assert (verify the results)
        self.assertEqual(return_value, output)

    def test_escape_tex_underscore(self):
        # Arrange (set up test environment)
        input = r"_"
        output = r"\_"

        # Act (actually perform what has to be done)
        return_value = escape_tex(input)

        # Assert (verify the results)
        self.assertEqual(return_value, output)

    def test_escape_tex_curly_left(self):
        # Arrange (set up test environment)
        input = r"{"
        output = r"\{"

        # Act (actually perform what has to be done)
        return_value = escape_tex(input)

        # Assert (verify the results)
        self.assertEqual(return_value, output)

    def test_escape_tex_curly_right(self):
        # Arrange (set up test environment)
        input = r"}"
        output = r"\}"

        # Act (actually perform what has to be done)
        return_value = escape_tex(input)

        # Assert (verify the results)
        self.assertEqual(return_value, output)

    def test_escape_tex_tilde(self):
        # Arrange (set up test environment)
        input = r"~"
        output = r"\texttt{\~{}}"

        # Act (actually perform what has to be done)
        return_value = escape_tex(input)

        # Assert (verify the results)
        self.assertEqual(return_value, output)

    def test_escape_tex_exp(self):
        # Arrange (set up test environment)
        input = r"^"
        output = r"\^{}"

        # Act (actually perform what has to be done)
        return_value = escape_tex(input)

        # Assert (verify the results)
        self.assertEqual(return_value, output)

    def test_escape_tex_backslash(self):
        # Arrange (set up test environment)
        input = r"\ "
        output = r"$\backslash$ "

        # Act (actually perform what has to be done)
        return_value = escape_tex(input)

        # Assert (verify the results)
        self.assertEqual(return_value, output)

    def test_escape_tex_full(self):
        # Arrange (set up test environment)
        input = r"& % $ # _ { } ~ ^ \ \today"
        output = (
            r"\& \% \$ \# \_ \{ \} \texttt{\~{}} \^{} $\backslash$ $\backslash$today"
        )

        # Act (actually perform what has to be done)
        return_value = escape_tex(input)

        # Assert (verify the results)
        self.assertEqual(return_value, output)
