# SPDX-License-Identifier: MIT

"""Just for linting."""

# Django imports
from django.test import TestCase

# app imports
from calingen.blubb import foo


class BlubbTest(TestCase):
    """Just for linting."""

    def test_foo(self) -> None:
        """Just for linting."""
        self.assertEqual(foo(1, 1), 2)
