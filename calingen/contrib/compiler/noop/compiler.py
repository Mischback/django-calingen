# SPDX-License-Identifier: MIT

"""The actual module with the plugin's payload."""


# Django imports
from django.http.response import HttpResponse

# app imports
from calingen.interfaces.plugin_api import TeXCompilerProvider


class NoOpCompiler(TeXCompilerProvider):
    """Do not compile TeX sources, but just return them in a view for copy/paste."""

    title = "NoOpCompiler"

    @classmethod
    def get_response(cls, tex_source):  # noqa: D102
        return HttpResponse(
            tex_source,
            headers={
                "Content-Type": "application/x-tex",
                "Content-Disposition": 'attachment; filename="foo.tex"',
            },
        )  # pragma: nocover
