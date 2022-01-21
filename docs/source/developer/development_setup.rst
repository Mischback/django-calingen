.. _calingen-dev-doc-setup-label:

#################
Development Setup
#################

This section is targeted at development of |calingen| itsself. It may not be
ideal for :ref:`developing plugins <calingen-dev-doc-plugins-label>`, though it
should be possible aswell.

********
Abstract
********

The `repository at GitHub`_ provides a stand-alone development environment
for |calingen|, depending on only two external tools: `Git`_ and `tox`_.

Additionally it is highly recommended to have ``make`` available on your
development system, as |calingen| provides a ``Makefile`` acting as
user-interface for the ``tox`` environments.

An actual installation of `Django`_ is **not required**, |calingen| provides
a ``tox`` environment to run the development source code of the application
in the context of a minimal Django project.

.. _repository at GitHub: https://github.com/Mischback/django-calingen/
.. _Git: https://git-scm.com/
.. _tox: https://github.com/tox-dev/tox
.. _Django: https://djangoproject.com


.. _calingen-dev-doc-setup-getting-started-label:

***************
Getting Started
***************

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


.. _calingen-dev-doc-setup-desc-label:

************
Description
************

Repository Layout
=================

::

  django-calingen/
    .github/                 # utility files for GitHub, including workflows
    .vscode/                 # configuration for VSCode
    calingen/                # Python module - the actual app
    docs/                    # documentation sources for Sphinx
    requirements/            # requirments files to be used with pip
    tests/                   # Python module - test suite
    .editorconfig            # configuration for supporting editors
    .flake8                  # configuration for flake8
    .gitignore               # ...
    .pre-commit-config.yaml  # configuration of pre-commit
    CHANGELOG.md             # ...
    LICENSE                  # MIT, actually
    Makefile                 # configuration for make
    pyproject.toml           # configuration for most of the tools
    README.md                # ...


Tools in Use
============

- **tox** (`tox@GitHub <https://github.com/tox-dev/tox>`_): Actually all tools are run
  from within ``tox``, see :ref:`calingen-dev-doc-setup-desc-tox-env-label` for
  a detailled description of the provided environments and how they relate to
  given development tasks.
- **pre-commit** (`pre-commit@GitHub <https://github.com/pre-commit/pre-commit>`_):
  Several code quality tools are run by ``pre-commit``. If activated as
  described in :ref:`calingen-dev-doc-setup-getting-started-label`, these tools
  are run on every commit, maintaining a high quality codebase.

  - **black** (`black@GitHub <https://github.com/psf/black>`_): Python code
    formatter. No configuration is provided, meaning the code formatting is
    handed over fully to ``black``.
  - **isort** (`isort@GitHub <https://github.com/PyCQA/isort>`_): Sort imports
    in Python source code. Configuration is included in ``pyproject.toml``.
  - **flake8** (`flake8@GitHub <https://github.com/PyCQA/flake8>`_): Python
    linter. Configuration is provided by ``.flake8``. The following plugins are
    run:

      - flake8-bugbear (`flake8-bugbear@GitHub <https://github.com/PyCQA/flake8-bugbear>`_)
      - flake8-docstrings (`flake8-docstrings@GitHub <https://github.com/PyCQA/flake8-docstrings>`_)
      - flake8-django (`flake8-django@GitHub <https://github.com/rocioar/flake8-django>`_)
      - flake8-assertive (`flake8-assertive@GitHub <https://github.com/jparise/flake8-assertive>`_)

  - **bandit** (`bandit@GitHub <https://github.com/PyCQA/bandit>`_): Python
    security linter. No configuration is provided.
  - **djlint** (`djlint@GitHub <https://github.com/Riverside-Healthcare/djLint>`_):
    Linting for Django's HTML templates. Configuration is included in
    ``pyproject.toml``.
  - **doc8** (`doc8@GitHub <https://github.com/PyCQA/doc8>`_): Style checker for rST
    source files. No configuration is provided.

  The whole ``pre-commit`` configuration can be found in
  ``.pre-commit-config.yaml``. It includes some more *hooks* that are not
  Python-specific.

  ``pre-commit`` is run as part of the project's *CI configuration* aswell, see
  :ref:`calingen-dev-doc-setup-desc-gh-actions-label` for details.
- **coverage.py** (`coverage.py@GitHub <https://github.com/nedbat/coveragepy>`_):
  Measuring code coverage of the test suite.

  Configuration is provided in ``pyproject.toml``. This is also run in *CI* and
  reported to
  `Coveralls <https://coveralls.io/github/Mischback/django-calingen>`_
- **flit** (`flit@GitHub <https://github.com/pypa/flit>`_): Building and
  publishing Python packages to PyPI.

  ``flit`` is run from a *GitHub Action*, see
  :ref:`calingen-dev-doc-setup-desc-gh-actions-label` for details.


.. _calingen-dev-doc-setup-desc-tox-env-label:

``tox`` Environments
====================


.. _calingen-dev-doc-setup-desc-gh-actions-label:

GitHub Actions (Continuous Integration)
=======================================

.. |calingen| replace:: **django-calingen**
