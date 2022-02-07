# SPDX-License-Identifier: MIT

"""Implementation of :class:`~calingen.interfaces.plugin_api.CompilerProvider` that directly serves HTML-based layouts and provides the source code of other rendered layouts as file download.

This compiler **is able to handle all types of layouts**, meaning it supports
all layout source languages (as no real compilation is performed).

This makes this compiler a suitable choice for the ``"default"`` compiler in
**django-calingen**'s settings (see :attr:`~calingen.settings.CALINGEN_COMPILER`).

Warnings
--------
The file extension of the (downloadable) file is determined by using the
layout's ``layout_type`` attribute (see
:class:`calingen.interfaces.plugin_api.LayoutProvider`) in combination with
:attr:`calingen.contrib.compilers.html_or_download.compiler.SOURCE_TYPE_LOOKUP`.

Notes
-----
The layout's ``layout_type`` attribute is also used to determine, if the given
source is of type ``HTML`` and can thus be served directly.
"""
