# SPDX-License-Identifier: MIT

"""App-specific exceptions."""


class CalingenException(Exception):
    """Base class for all app-specific exceptions."""


class CallingenInterfaceException(CalingenException):
    """Base class for all exceptions of the ``interfaces`` module."""
