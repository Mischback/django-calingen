# SPDX-License-Identifier: MIT

"""The actual module with the plugin's payload."""


# Django imports
from django.shortcuts import render

# app imports
from calingen.interfaces.plugin_api import CompilerProvider


class CopyPasteCompiler(CompilerProvider):
    """Do not compile sources, but just return them in a view for copy/paste."""

    title = "CopyPasteCompiler"

    @classmethod
    def get_response(cls, source):  # noqa: D102
        context = {"rendered_source": source}
        return render(
            None,
            template_name="calingen/contrib/compiler_copypaste.html",
            context=context,
        )  # pragma: nocover
