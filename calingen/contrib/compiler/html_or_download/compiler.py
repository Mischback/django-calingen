# SPDX-License-Identifier: MIT

"""The actual module with the plugin's payload."""


# Django imports
from django.http.response import HttpResponse

# app imports
from calingen.interfaces.plugin_api import CompilerProvider

SOURCE_TYPE_LOOKUP = {
    "plain": ("txt", "text/plain; charset=UTF-8"),
    "markdown": ("md", "text/markdown; charset=UTF-8"),
    "rst": ("rst", "text/x-rst"),
    "tex": ("tex", "application/x-tex"),
}


class HtmlOrDownloadCompiler(CompilerProvider):
    """Provide an HTTP response, if the layout renders to HTML or a file download otherwise."""

    title = "HtmlOrDownloadCompiler"

    @classmethod
    def get_response(cls, source, layout_type=None):  # noqa: D102
        if layout_type is not None:
            if layout_type == "html":
                return HttpResponse(source)
            else:
                try:
                    file_extension = SOURCE_TYPE_LOOKUP[layout_type][0]
                    content_type = SOURCE_TYPE_LOOKUP[layout_type][1]
                except KeyError:
                    file_extension = SOURCE_TYPE_LOOKUP["plain"][0]
                    content_type = SOURCE_TYPE_LOOKUP["plain"][1]
        else:
            file_extension = SOURCE_TYPE_LOOKUP["plain"][0]
            content_type = SOURCE_TYPE_LOOKUP["plain"][1]

        return HttpResponse(
            source,
            headers={
                "Content-Type": content_type,
                "Content-Disposition": 'attachment; filename="calingen_generated_source.{}"'.format(
                    file_extension
                ),
            },
        )  # pragma: nocover
