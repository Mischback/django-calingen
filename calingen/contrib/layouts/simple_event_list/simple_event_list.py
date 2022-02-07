# SPDX-License-Identifier: MIT

""":class:`~calingen.interfaces.plugin_api.LayoutProvider` implementation for a simple event list.

Warnings
--------
This layout is included in **django-calingen**'s CI test setup, mainly to verify
that the :func:`TeX escaping <calingen.templatetags.calingen_escape.escape_tex>`
is working.

This may be object to future changes.
"""

# app imports
from calingen.interfaces.plugin_api import LayoutProvider


class SimpleEventList(LayoutProvider):
    """The actual implementation of the layout.

    Nothing fancy here,
    :meth:`~calingen.contrib.layouts.simple_event_list.simple_event_list.SimpleEventList.prepare_context`
    is just used to group the provided
    :class:`calingen.interfaces.data_exchange.CalendarEntryList` by month.

    Warnings
    --------
    The provided templates create a document targeted at German users. You may
    override the templates to (fully) support other languages.

    Notes
    -----
    To customize the generated TeX-sources, the following templates may be
    overridden:

    - ``simple_event_list/tex/base.tex``: Speaking in TeX-terms: the preamble of
      the document, including package definitions.
    - ``simple_event_list/tex/simple_event_list.tex``: Speaking in TeX-terms:
      the document's body.
    - ``simple_event_list/tex/single_entry_line.tex``: The actual
      TeX-representation of a
      :class:`calingen.interfaces.data_exchange.CalendarEntry`.
    """

    name = "Simple Event List"
    paper_size = "a4"
    orientation = "portrait"
    layout_type = "tex"
    _template = "simple_event_list/tex/simple_event_list.tex"

    @classmethod
    def prepare_context(cls, context):
        """Pre-process the ``entries`` to group them by month."""
        entries = context.pop("entries", [])

        # put each month's entries in a dedicated list
        processed_entries = []
        try:
            loop_month = entries[0].timestamp.month
        except IndexError:
            loop_month = "No Entries"

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
