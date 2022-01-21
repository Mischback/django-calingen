.. _calingen-dev-doc-setup-label:

#################
Development Setup
#################

This section is targeted at development of |calingen| itsself. It may not be
ideal for developing :ref:`plugins <calingen-dev-doc-plugins-label>`, though it
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
.. _Git: https://git.org?FIXME
.. _tox: https://github.com/tox/tox?FIXME
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

.. |calingen| replace:: **django-calingen**
