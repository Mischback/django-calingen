# SPDX-License-Identifier: MIT

"""The actual module with the plugin's payload."""


# Django imports
from django.http.response import HttpResponse

# app imports
from calingen.interfaces.plugin_api import CompilerProvider


class NoOpCompiler(CompilerProvider):
    """Do not compile sources, but just return them in a view for copy/paste."""

    title = "NoOpCompiler"

    @classmethod
    def get_response(cls, source):  # noqa: D102
        return HttpResponse(
            source,
            headers={
                "Content-Type": "application/x-tex",
                "Content-Disposition": 'attachment; filename="foo.tex"',
            },
        )  # pragma: nocover
