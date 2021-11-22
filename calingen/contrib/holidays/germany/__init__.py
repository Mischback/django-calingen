# SPDX-License-Identifier: MIT

""":class:`~calingen.interfaces.plugin_api.EventProvider` implementations for german holidays."""

# app imports
from calingen.interfaces.plugin_api import EventProvider


class GermanyFederal(EventProvider):
    """Provides federal holidays of Germany."""

    title = "Germany Federal Holidays"

    @classmethod
    def resolve(cls, year):  # noqa: D102
        return "foo"
