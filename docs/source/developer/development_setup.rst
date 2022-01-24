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
- **Sphinx** (`Sphinx@GitHub <https://github.com/sphinx-doc/sphinx>`_): The
  documentation is intended to be published on RtD, which uses ``Sphinx``.
  Configuration is provided in ``docs/source/conf.py``.


.. _calingen-dev-doc-setup-desc-tox-env-label:

``tox`` Environments
====================

``tox``'s configuration is included in ``pyproject.toml``.

Besides running the test suite, ``tox`` is used for every given (local)
development task, including running the app in a (minimal) Django project.

During *Continuous Integration* (see
:ref:`calingen-dev-doc-setup-desc-gh-actions-label` for details), ``tox`` is
used aswell.


``testenv``
-----------

The actual (default) testing environment. Intended to be run by Continuous
Integration (and is in fact used in
:ref:`the app's CI workflows <calingen-dev-doc-setup-desc-gh-actions-label>`).

Runs the test suite (under ``coverage.py``).


``testenv:django``
------------------

Provides a minimal Django project, setup for development of the app itsself.
This allows to run any ``django-admin`` command against the actual source code
of the repository.

The required ``settings`` module and *url configuration* are located in
``tests/util/settings_dev.py`` and ``tests/util/urls_dev.py``.

To make Django's authentication work, the required login template is provided
in ``tests/util/templates/registration/login.html``.

Most *common* development-related ``django-admin`` commands are included in the
project's ``Makefile`` and will use this environment internally, e.g.
``make django/runserver`` will run Django's internal development server on
``0:8000`` (see :ref:`calingen-dev-doc-setup-desc-makefile-label`).

Packages are installed from ``requirements/development.txt``.


``testenv:djangosuperuser``
---------------------------

Just an extension to ``testenv:django`` to create a superuser in the Django
project.

``username`` and ``password`` are hardcoded in ``tox``'s configuration, as they
are strictly for development purposes anyway.

- username: ``admin``
- password: ``foobar``


``testenv:installation``
------------------------

During Continuous Integration it is verified, that the package is actually
installable.

This is handled by this environment. It will use ``pip`` to install the app's
package from a local directory (where a previous step in the workflow placed
the built package).


``testenv:util``
----------------

This environment runs all utility software during development and CI.

``pre-commit`` (including its *hooks*) and ``flit`` are run from this
environment, aswell as ``coverage.py``'s commands that are not directly related
to collecting coverage information (those are run from the test environments).

Packages are installed from ``requirements/util.txt``.


``testenv:sphinx``
------------------

Locally build and view the app's documentation using ``sphinx``.

Packages are installed from ``requirements/documentation.txt``.


``testenv:sphinx-serve``
------------------------

Just an extension of ``testenv:sphinx`` that launches Python's built-in
``http.server`` in the output directory.

*Has to be provided as its own environment, because it should change into the
build directory. Internally, ``testenv:sphinx`` is reused completely.*


``testenv:testing``
-------------------

Runs the test suite for development purposes.

While running ``tox`` will actually run the test suite against multiple
versions of Python (if available) and Django, this environment only runs on the
hosts main Python version and the highest Django version (as specified in
``requirements/common.txt``).


.. _calingen-dev-doc-setup-desc-makefile-label:

Makefile
========


.. _calingen-dev-doc-setup-desc-gh-actions-label:

GitHub Actions (Continuous Integration)
=======================================

GitHub Actions are used as Continuous Integration platform.

As of now, two workflows are provided:

CI Default Branch
-----------------

``.github/workflows/ci-default.yml``

This is the actual integration workflow.

It is run on the *default branch*, which is ``development`` and on any pull
request against this branch.

The workflow will run code quality tools (``black``, ``flake8``, ``bandit``),
build a PyPI-compatible package (using ``flit``), run the test suite in a
matrix of different operating systems, Python and ``Django`` versions,
collecting covearge information (by ``coverage.py``), try to  install the
package on each operating system and Python version and finally report all
collected coverage information to *Coveralls*.

As of now, the following test matrix is used:

- **operating systems** (defined in *workflow file*): ``windows-latest``,
  ``ubuntu-latest`` (for Linux)
- **Python versions** (defined in *workflow file*): ``3.7``, ``3.8``, ``3.9``,
  ``3.10``
- **Django verions** (defined in *tox configuration*): ``3.1``, ``3.2``,
  ``4.0``

.. include:: ../includes/ci-matrix.rst.txt

The workflow actually relies heavily on the project's
:ref:`tox environments <calingen-dev-doc-setup-desc-tox-env-label>` internally.


CI Release
----------

``.github/workflows/ci-release.yml``

This workflow will release the packaged app to PyPI.

Internally, it uses ``flit`` from inside a
:ref:`tox environment <calingen-dev-doc-setup-desc-tox-env-label>`.

.. warning::
  To authenticate with https://pypi.org, a token is used. This has to be
  provided using a repository secret named ``PYPI_REPO_TOKEN``.

.. |calingen| replace:: **django-calingen**
