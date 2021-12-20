# SPDX-License-Identifier: MIT

"""Provides app-specific test classes."""

# Python imports
import os
from pathlib import Path

# Django imports
from django.conf import settings
from django.test import SimpleTestCase, TestCase, tag
from django.test.testcases import TransactionTestCase

# app imports
from calingen.interfaces.data_exchange import CalendarEntryList
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

    def get_entries(self, target_year):
        """Fetch some entries from the fixture."""
        profile = Profile.calingen_manager.get(pk=1)  # Alice

        all_entries = CalendarEntryList()
        internal_events = Event.calingen_manager.get_calender_entry_list(
            user=profile.owner, year=target_year
        )
        plugin_events = profile.resolve(year=target_year)
        all_entries.merge(internal_events)
        all_entries.merge(plugin_events)

        return all_entries.sorted()

    def write_tex_to_tmp(self, rendered_tex, tex_filename):
        """Create a TeX source file for compilation."""
        working_dir_path = os.path.join(settings.PROJECT_ROOT, "tmp_compilation")
        Path(working_dir_path).mkdir(parents=True, exist_ok=True)

        fullpath = os.path.join(working_dir_path, tex_filename)

        with open(fullpath, "x", encoding="utf-8") as output_file:
            output_file.write(rendered_tex)

        return os.path.exists(fullpath)
