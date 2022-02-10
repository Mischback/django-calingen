# SPDX-License-Identifier: MIT

"""Calingen's implementations of :class:`django.db.models.Model`.

In the context of a Django application, ``models`` define the app's core data,
that is persisted in a database layer (abstracted by DJango's ORM).

This package also includes model-related implementations of
:class:`django.db.models.QuerySet`, :class:`django.db.models.Manager` and
:class:`django.forms.ModelForm`.

Notes
-----
It's kind of recommended to have *fat models* in a Django application, that
handle most of the app's business logic.

However, *fat models* might lead to models, that are *too tightly* connected to
each other.

Calingen's models aim to present and manage the app's data and enable working
with that data.
"""

# app imports
from calingen.models.event import Event  # noqa: F401
from calingen.models.profile import Profile  # noqa: F401
