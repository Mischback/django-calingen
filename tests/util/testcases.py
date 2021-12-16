# SPDX-License-Identifier: MIT

"""Provides app-specific test classes."""

# Python imports
import os
import subprocess  # nosec: required for TeX compilation
import tempfile

# Django imports
from django.test import SimpleTestCase, TestCase, tag
from django.test.testcases import TransactionTestCase

# app imports
from calingen.interfaces.data_exchange import CalenderEntryList
from calingen.models.event import Event
from calingen.models.profile import Profile


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


class CalingenORMTransactionTestCase(TransactionTestCase):  # noqa: D101
    fixtures = ["tests/util/fixtures/test_data.json"]


@tag("requires_system_tex")
class CalingenTeXLayoutCompilationTestCase(CalingenORMTestCase):
    """These tests require a working TeX installation on the system and are skipped by default."""

    def run_compilation(self, rendered_tex, test_filebasename):
        """Execute the actual compilation with lualatex."""
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

            return os.path.exists(test_output_filename)

    def get_entries(self, target_year):
        """Fetch some entries from the fixture."""
        profile = Profile.calingen_manager.get(pk=1)  # Alice

        all_entries = CalenderEntryList()
        internal_events = Event.calingen_manager.get_calender_entry_list(
            user=profile.owner, year=target_year
        )
        plugin_events = profile.resolve(year=target_year)
        all_entries.merge(internal_events)
        all_entries.merge(plugin_events)

        return all_entries.sorted()
