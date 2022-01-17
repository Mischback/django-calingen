# SPDX-License-Identifier: MIT

"""Implementation of :class:`~calingen.interfaces.plugin_api.CompilerProvider` that provides the source code of the rendered layout as file download.

This compiler **is able to handle all types of layouts**, meaning it supports
all layout source languages (as no real compilation is performed).

This makes this compiler a suitable choice for the ``"default"`` compiler in
**django-calingen**'s settings (see :attr:`~calingen.settings.CALINGEN_COMPILER`).

Warnings
--------
The file extension of the (downloadable) file is determined by using the
layout's ``layout_type`` attribute (see
:class:`calingen.interfaces.plugin_api.LayoutProvider`) in combination with
:attr:`calingen.contrib.compilers.download.compiler.SOURCE_TYPE_LOOKUP`.
"""
