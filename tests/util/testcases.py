# SPDX-License-Identifier: MIT

"""Provides app-specific test classes."""

# Django imports
from django.test import SimpleTestCase, TestCase


# Add documentation if there is acutally code!
class CalingenTestCase(SimpleTestCase):  # noqa: D101
    pass


class CalingenORMTestCase(TestCase):  # noqa: D101
    """Support testing with fixture data.

    What is included in this test fixture?
    ======================================
    - 4 user instances (django.contrib.auth.User)
        - Alice, Bob, Charly (superuser), Egon
        - all passwords: "foobar"
    - 3 Profile instances (calingen.models.profile.Profile)
        - Alice, Bob, Charly
    - 4 Events (calingen.models.event.Event)
        - Alice (3 Events)
        - Bob (1 Event)

    Command to dump the data
    ------------------------
    > tox -q -e django -- \
        dumpdata \
            --all \
            --indent 2 \
            --exclude admin.logentry \
            --exclude auth.permission \
            --exclude sessions.session \
            --exclude contenttypes.contenttype \
            --output tests/util/fixtures/test_data.json
    """

    fixtures = ["tests/util/fixtures/test_data.json"]
