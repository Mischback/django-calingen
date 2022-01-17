# SPDX-License-Identifier: MIT

"""Implementation of :class:`~calingen.interfaces.plugin_api.CompilerProvider` that presents the source code of the rendered layout ready for copy/paste.

This compiler **is able to handle all types of layouts**, meaning it supports
all layout source languages (as no real compilation is performed).

This makes this compiler a suitable choice for the ``"default"`` compiler in
**django-calingen**'s settings (see :attr:`~calingen.settings.CALINGEN_COMPILER`).

Notes
-----
The compiler uses the template ``calingen/contrib/compiler_copypaste.html`` to
present the rendered source code.

This template may be substituted in a real project.
"""
