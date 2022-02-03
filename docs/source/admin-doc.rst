.. _calingen-admin-doc-label:

###########################
Administrator Documentation
###########################

**********************
Installation and Setup
**********************

Requirements
============

Platform, Python and Django
---------------------------

.. note::
  The following listing summarizes what is tested during development, using
  GitHub Actions as a CI environment.

  You might be able to run in different environments and on different
  platforms (looking at you, ``macos``).

**Python** is supported from version **3.7**. **Django** is supported from
version **3.1**.

.. include:: includes/ci-matrix.rst.txt

.. note::
  Python 3.7 and 3.8 are not tested on Windows hosts, because these Python
  versions are not shipped with the required SQLite extension to handle
  JSON fields.

  This is not relevant if you're using another DB (Postgre, MariaDB).

  See `the Django wiki <https://code.djangoproject.com/wiki/JSON1Extension>`_
  for a detailled walkthrough on how to activate the required extension to
  SQLite on Python 3.7 / 3.8 for Windows hosts.

  |calingen| is assumed to run on Python 3.7 / 3.8 on Windows hosts.


Additional Python Packages
--------------------------

Besides Django, there is - as of now - only one additional dependency, namely
``python-dateutil``. See :source:`requirements/common.txt` for details.


Installation
============

Configuration
=============

Project's ``settings`` Module
-----------------------------

Project's ``urls`` Configuration
--------------------------------


Checks
======


*************************
Providing External Events
*************************


.. _calingen-admin-doc-layouts-label:

*****************
Providing Layouts
*****************


.. _calingen-admin-doc-compilers-label:

*******************
Providing Compilers
*******************

DUMMY
=====

Configuration
-------------

The app-specific setting :attr:`~calingen.settings.CALINGEN_COMPILER` is used
to determine, which layout will be processed by a given compiler.

Please refer to :attr:`~calingen.settings.CALINGEN_COMPILER` for details on
this setting and accepted values.



Included Compilers
==================

|calingen| provides some compilers out of the box. They are included in
``calingen.contrib.compilers``.

TODO: List the available compilers here, with a short description of their
      features (rST glossary?)

The included compilers are all ready to be used as ``"default"`` compiler,
they are capable of handling any type of layout.

.. note::
  If :attr:`~calingen.settings.CALINGEN_COMPILER` is not explicitly included
  in the project's settings module, the ``CopyPasteCompiler`` is used as the
  app's ``"default"`` compiler.


***************************
Modify calingen's Templates
***************************

|calingen| is developed to be as pluggable as possible. This means: there are
basic templates included with the app, but these are mainly focused on
development.

To actually deploy the app within a Django project, you will want to replace
the app's templates by overriding them.


App Templates vs. Project Templates
===================================

Most likely your project will be setup to include app directories while
looking for templates (by specifying ``"APP_DIRS": True`` within
:setting:`TEMPLATES`).

This will let |calingen| work *out of the box* but enables your project to
easily modify the templates.

Just create a ``calingen`` folder within your project's ``templates``
directory (as specified by ``"DIRS"`` within :setting:`TEMPLATES`) and you're
good to go.

.. note::
  See :ref:`calingen-admin-doc-views-urls-templates-label` for a table that
  provides the matching between urls, the corresponding views and their
  templates.


.. _calingen-admin-doc-views-urls-templates-label:

Views, URLs and Templates
=========================



.. |calingen| replace:: **django-calingen**
.. _PyPI: https://pypi.org
