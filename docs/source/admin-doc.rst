.. _calingen-admin-doc-label:

###########################
Administrator Documentation
###########################

.. note::
  This document is the short reference on how to make |calingen| work in a
  Django project. For a more detailled guide, see
  :ref:`calingen-cookbook-setup-step-by-step-label`.

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
|calingen| is installable from `PyPI <https://pypi.org>`_. ::

  pip install django-calingen


Configuration
=============

Project's ``settings`` Module
-----------------------------

Include ``'calingen'`` into :setting:`INSTALLED_APPS`: ::

  INSTALLED_APPS = [
    '...
    'calingen',  # <- added!
  ]

.. note::
  While the Python package of the app is named ``django-calingen``, the actual
  app is just named ``calingen``.

  This is common for pluggable Django applications

Please note that :ref:`calingen-cookbook-ingredients-layouts-label` and
:ref:`calingen-cookbook-ingredients-eventprovider-label` are provided as
standalone apps and **must** be included in :setting:`INSTALLED_APPS` aswell.
See the respective installation instructions.

It is assumed that the project is set up to look in *applications directories*
for templates, as this is the default setting. Please refer to
:setting:`TEMPLATES`.


Project's ``urls`` Configuration
--------------------------------

Include the app's *urls* into the project's *url configuration*: ::

  from django.urls import include, path

  urlpatterns = [
      ...
      path('calingen/', include('calingen.urls')),  # <- added!
  ]


App-specific Configuration Options
----------------------------------

There are :mod:`some configuration options <calingen.settings>`, which can be
set using the project's ``settings`` module.

All of them are providing sane default values.

:ref:`calingen-cookbook-setup-step-by-step-settings` has some more details on
that topic.


Checks
======

|calingen| does provide some contributions to
:djangodoc:`Django's System check framework <topics/checks/>`, basically to
check app-specific configuration values. See :mod:`calingen.checks` for
details.


***************************
Modify calingen's Templates
***************************

|calingen| is developed to be as pluggable as possible. This means: there are
basic templates included with the app, but these are mainly focused on
development.

To actually deploy the app within a Django project, you will want to replace
the app's templates by overriding them.

:ref:`calingen-cookbook-modify-templates-label` provides additional information
that should suffice as a starting point.


.. |calingen| replace:: **django-calingen**
.. _PyPI: https://pypi.org
