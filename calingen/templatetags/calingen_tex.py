# SPDX-License-Identifier: MIT

"""Provide TeX-specific templatetags."""

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
    """Escape TeX control characters/sequences."""
    value = RE_BACKSLASH.sub(r"\\backslash", value)
    value = RE_BATCH.sub(r"\\\1", value)
    value = RE_EXP.sub(r"\^{}", value)
    value = RE_TILDE.sub(r"\\texttt{\~{}}", value)
    value = RE_BACKSLASH_FIX.sub(r"$\1$", value)

    return value
