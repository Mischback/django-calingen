# SPDX-License-Identifier: MIT

"""The actual module with the plugin's payload."""


# Django imports
from django.http.response import HttpResponse

# app imports
from calingen.interfaces.plugin_api import CompilerProvider

SOURCE_TYPE_LOOKUP = {
    "tex": ("tex", "application/x-tex"),
}


class DownloadCompiler(CompilerProvider):
    """Do not compile sources, but provide them as file download."""

    title = "DownloadCompiler"

    @classmethod
    def get_response(cls, source, layout_type=None):  # noqa: D102
        if layout_type is not None:
            content_type = SOURCE_TYPE_LOOKUP[layout_type][1]
            file_extension = SOURCE_TYPE_LOOKUP[layout_type][0]

        return HttpResponse(
            source,
            headers={
                "Content-Type": content_type,
                "Content-Disposition": 'attachment; filename="calingen_generated_source.{}"'.format(
                    file_extension
                ),
            },
        )  # pragma: nocover
