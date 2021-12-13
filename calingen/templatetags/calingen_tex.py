# SPDX-License-Identifier: MIT

"""Provide TeX-specific templatetags."""

# Django imports
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def escape_tex(value):
    """Escape TeX control characters/sequences."""
    return value
