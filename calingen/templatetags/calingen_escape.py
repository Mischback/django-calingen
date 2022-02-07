# SPDX-License-Identifier: MIT

"""App-specific templatetags for escaping strings in templates.

Calingen is intended to support various types of layouts, meaning the app is
able to support several *target languages* of templates (e.g. TeX, HTML, ...).

Different *target languages* require different strings to be escaped. All of
these are provided with this module.

Notes
-----
The required regular expressions to escape strings are compiled at module level
and may be re-used. This should boost performance during template processing.

An actual ``filter`` for HTML is not provided, this should already be covered
by Django's codebase.
"""

# Python imports
import re

# Django imports
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

RE_BACKSLASH = re.compile(r"\\")
"""RegEx to *find* backslashes (``\``)."""  # noqa: W605

RE_EXP = re.compile(r"\^")
"""RegEx to *find* carets (``^``)."""

RE_TILDE = re.compile(r"~")
"""RegEx to *find* tildes (``~``)."""

RE_TEX_CHARS = re.compile(r"([$#&%_{}])")
"""RegEx to *find* a bunch of TeX special characters (``$#&%_{}``)."""

RE_TEX_BACKSLASH_FIX = re.compile(r"(\\backslash)")
"""This RegEx is used to **fix** *backslash* escaping in TeX templates."""


@register.filter
@stringfilter
def escape_tex(value):
    r"""Escape TeX control characters/sequences.

    Parameters
    ----------
    value : str
        The string to be cleaned from TeX control sequences.

    Returns
    -------
    str
        The cleaned / escaped string.

    Notes
    -----
    Special characters / sequences to be processed:

    ``& % $ # _ { } ~ ^ \``

    The list of special TeX characters is taken from StackOverflow
    (see https://tex.stackexchange.com/a/34586). Actually, the same thread has
    the (Pearl) regular expressions to substitute these special characters
    aswell (see https://tex.stackexchange.com/a/119383).
    """
    # The order of substitution *does* matter!
    value = RE_BACKSLASH.sub(r"\\backslash", value)
    value = RE_TEX_CHARS.sub(r"\\\1", value)
    value = RE_EXP.sub(r"\^{}", value)
    value = RE_TILDE.sub(r"\\texttt{\~{}}", value)
    value = RE_TEX_BACKSLASH_FIX.sub(r"$\1$", value)

    return value
