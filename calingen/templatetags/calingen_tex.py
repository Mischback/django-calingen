# SPDX-License-Identifier: MIT

"""Provide TeX-specific templatetags.

Notes
-----
The required regular expressions to escape strings for TeX are compiled at
module level and may be re-used. This should boost performance during template
processing.
"""

# Python imports
import logging
import re

# Django imports
from django import template
from django.template.defaultfilters import stringfilter

logger = logging.getLogger(__name__)

register = template.Library()

RE_BACKSLASH = re.compile(r"\\")
RE_BATCH = re.compile(r"([$#&%_{}])")
RE_EXP = re.compile(r"\^")
RE_TILDE = re.compile(r"~")
RE_BACKSLASH_FIX = re.compile(r"(\\backslash)")


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
    value = RE_BACKSLASH.sub(r"\\backslash", value)
    value = RE_BATCH.sub(r"\\\1", value)
    value = RE_EXP.sub(r"\^{}", value)
    value = RE_TILDE.sub(r"\\texttt{\~{}}", value)
    value = RE_BACKSLASH_FIX.sub(r"$\1$", value)

    return value
