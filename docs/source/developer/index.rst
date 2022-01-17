.. _calingen-dev-doc-label:

#######################
Developer Documentation
#######################


.. _calingen-dev-doc-setup-label:

*****************
Development Setup
*****************

This section is targeted at development of |calingen| itsself. It may not be
ideal for developing :ref:`plugins <calingen-dev-doc-plugins-label>`, though it
should be possible aswell.

Abstract
========

The `repository at GitHub`_ provides a stand-alone development environment
for |calingen|, depending on only two external tools: `Git`_ and `tox`_.

Additionally it is highly recommended to have ``make`` available on your
development system, as |calingen| provides a ``Makefile`` acting as
user-interface for the ``tox`` environments.

An actual installation of `Django`_ is **not required**, |calingen| provides
a ``tox`` environment to run the development source code of the application
in the context of a minimal Django project.

.. _repository at GitHub: https://github.com/Mischback/django-calingen/
.. _Git: https://git.org?FIXME
.. _tox: https://github.com/tox/tox?FIXME
.. _Django: https://djangoproject.com

.. _calingen-dev-doc-setup-getting-started-label:

Getting Started
===============

.. note::
  All following code / command samples assume the availability of ``git``,
  ``make`` and ``tox``.

  If you're running ``tox`` in its own virtual environment, this would be the
  right moment to activate it.

#. clone the repository::

   $ git clone https://github.com/Mischback/django-calingen.git
   $ cd django-calingen

#. activate pre-commit hooks for code quality::

   $ make util/pre-commit/install

#. trigger Django installation::

   $ make django/check

#. run the test suite::

   $ make dev/test

Congratulations! You're up and ready for development! If you're interested in
the juicy details of this setup, see
:ref:`the high level repo description <calingen-dev-doc-setup-desc-label>`
below.

Coding Style
============

The following sections describe the style conventions for all source code
inside of the repository.

They should be considered *guidelines*, you're free to do whatever you desire.
However, some of them are actually checked during CI, causing builds to fail.

If you activated ``pre-commit`` as per
:ref:`Getting Started <calingen-dev-doc-setup-getting-started-label>`, you
should be good to go!

Python Source Code
------------------

- The Python source code is formatted using `black`_; this basically means:
  You should not need to care about code formatting.
- As a guideline: aim to reuse as much of the Django framework as possible
  (that's the idea of using a framework, isn't it?).
- Testing is important! Cover your code with unit tests.
- Provide documentation for your code. `flake8`_ is configured to highlight
  missing documentation.

.. _black: https://github.com/psf/black
.. _flake8: https://github.com/PyCQA/flake8

Python Docstrings
-----------------

Additional Documentation
------------------------

Git Commit Messages
-------------------

- highly recommended article: `How to write a Git Commit Message`_
- **tl;dr**:

  - Separate subject from body with one blank line
  - Limit the subject line to 50 characters
  - Capitalize the subject line
  - Do not end the subject line with a period
  - Use the imperative mood in the subject line
  - Wrap the body at around 72 characters
  - Use the body to explain *what* and *why* vs. *how*

- As a general guideline: the commit subject line should finish this sentence:

  | *If applied, this commmit will* **your subject line here**

.. _How to write a Git Commit Message: https://chris.beams.io/posts/git-commit/


.. _calingen-dev-doc-setup-desc-label:

Description
===========


***************
App's Internals
***************


.. _calingen-dev-doc-plugins-label:

**********
Plugin API
**********

.. _calingen-dev-doc-plugins-eventprovider-label:

``EventProvider`` Development
=============================


.. _calingen-dev-doc-plugins-layoutprovider-label:

``LayoutProvider`` Development
==============================


.. _calingen-dev-doc-plugins-compilerprovider-label:

``CompilerProvider`` Development
================================




.. |calingen| replace:: **django-calingen**
