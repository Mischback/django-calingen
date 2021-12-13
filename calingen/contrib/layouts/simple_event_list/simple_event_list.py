# SPDX-License-Identifier: MIT

""":class:`~calingen.interfaces.plugin_api.LayoutProvider` implementation for a simple event list."""

# app imports
from calingen.interfaces.plugin_api import LayoutProvider


class SimpleEventList(LayoutProvider):
    """A very simple implementation of a list of events."""

    name = "Simple Event List"
    paper_size = "a4"
    orientation = "portrait"
    _template = "simple_event_list/tex/simple_event_list.tex"

    @classmethod
    def prepare_context(cls, context):  # noqa: D102
        entries = context.pop("entries")

        # put each month's entries in a dedicated list
        processed_entries = []
        loop_month = entries[0].timestamp.month
        month_list = []
        for entry in entries:
            if entry.timestamp.month != loop_month:
                processed_entries.append(month_list)
                month_list = []
                loop_month = entry.timestamp.month
            month_list.append(entry)
        if month_list:
            processed_entries.append(month_list)

        context["entries"] = processed_entries
        return context
