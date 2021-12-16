# SPDX-License-Identifier: MIT

"""The actual package with the plugin's payload."""


# app imports
from calingen.interfaces.plugin_api import TeXCompilerProvider


class NoOpCompiler(TeXCompilerProvider):
    """Do not compile TeX sources, but just return them in a view for copy/paste."""

    title = "NoOpCompiler"

    @classmethod
    def get_response(cls, tex_source):  # noqa: D102
        raise NotImplementedError("Just verify that the compiler is called!")
