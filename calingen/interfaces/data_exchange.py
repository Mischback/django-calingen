# SPDX-License-Identifier: MIT

"""Provides data exchange formats."""

# Python imports
from collections import namedtuple

CalenderEntry = namedtuple("CalenderEntry", "title type start")
"""This data structure is used to pass calender entries around.

Warnings
--------
This data structure does not provide any validation of its values / fields.

Following EAFP: the consuming code **must ensure** that the received data is of
the expected type.

Notes
-----
The structure contains an entries ``title``, ``type`` and its ``start`` date and
time (as :py:obj:`datetime.datetime`).

This is implemented as :py:obj:`collections.namedtuple`.
"""
