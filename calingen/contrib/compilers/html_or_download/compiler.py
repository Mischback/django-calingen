# SPDX-License-Identifier: MIT

"""The actual implementation of the compiler.

This is a simple extension of
:class:`calingen.contrib.compilers.download.compiler.DownloadCompiler` that
serves HTML-based content directly.
"""


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
"""A :py:obj:`dict` that provides meta information for file downloads.

The :meth:`~calingen.contrib.compilers.download.compiler.DownloadCompiler.get_response`
uses this :py:obj:`dict` to determine the file extension and MIME type for the
download, based on the layout's ``layout_type`` attribute (see
:class:`calingen.interfaces.plugin_api.LayoutProvider`).
"""


class HtmlOrDownloadCompiler(CompilerProvider):
    """Provide an HTTP response, if the layout renders to HTML or a file download otherwise."""

    title = "HtmlOrDownloadCompiler"

    @classmethod
    def get_response(cls, source, layout_type=None):  # noqa: D102
        if layout_type is not None:  # pragma: nocover
            if layout_type == "html":
                return HttpResponse(source)
            else:
                try:
                    file_extension = SOURCE_TYPE_LOOKUP[layout_type][0]
                    content_type = SOURCE_TYPE_LOOKUP[layout_type][1]
                except KeyError:
                    file_extension = SOURCE_TYPE_LOOKUP["plain"][0]
                    content_type = SOURCE_TYPE_LOOKUP["plain"][1]
        else:  # pragma: nocover
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
