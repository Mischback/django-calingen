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
  for a detailled walkthrough.

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

What is a Layout?
=================

|calingen| uses *layouts* to format the actual calendar inlays. Basically
they are sets of templates used to present the app's data (which is a list of
events for a given user).

Technically, *layouts* are provided as standalone Django applications that
register themselves with |calingen| and are integrated into the general
workflow of the app (see :ref:`calingen-user-doc-generate-inlays-label`).

.. note::
  Even more technically: Layouts are implementations of the app's plugin mount
  point :class:`~calingen.interfaces.plugin_api.LayoutProvider`. See
  :ref:`calingen-dev-doc-plugins-layoutprovider-label` for details.

*Layouts* are **rendered** to their respective result. This means, that the
project's template engine is used to **render** a layout's templates to a
:py:obj:`string <str>` which can be processed further by a compiler (see
:ref:`calingen-admin-doc-compilers-label` and :setting:`TEMPLATES`).


How to Make Layouts Available?
==============================

Because layouts are just Django applications, they may be installed like any
other application into the Django project: just add them to the project's
settings module in :setting:`INSTALLED_APPS`.

Obviously, this requires the layout to be actually available in your project's
Python environment.

Layouts may be provided as source code (i.e. by a GitHub repository) or as an
actual installable Python package (i.e. provided using `PyPI`_). If you want to
include third party layouts, make sure to follow their specific installation
instructions.

That's it. Once the layout is successfully installed and included in
:setting:`INSTALLED_APPS`, it will be available for selection.


Included Layouts
================

|calingen| provides some layouts out of the box. They are included in
``calingen.contrib.layouts``.

.. warning::
  While these layouts are *available* when |calingen| is installed, they must
  be activated manually by including them in :setting:`INSTALLED_APPS`.

Simple Event List
  This is just an easy example of a layout, that processes the given list of
  Event instances (both, user-provided and externally provided) and creates
  TeX sources for compilation with a TeX compiler (like ``pdflatex``).

  The layout does not provide a configuration form, as it does not have any
  options.

  During processing, the Event instances are grouped by their month.

Year By Week
  This slightly more complex example actually creates a list of all days of
  the year, include Event instances and then creates TeX sources.

  There is no configuration form.

  It visualizes, how a complete calendar can be generated.

Lineatur
  This layout may be used to generate ruled paper sheets to augment a
  calendar.

  It will generate HTML sources (and might even provide a valid HTTP response
  in combination with an appropriate compiler).

  This layout provides a configuration form.


These layouts are developed against Django's default template engine / syntax.

.. note::
  The included layouts may be considered *example implementations*. They are
  working but they are not intended to cover all use cases.

  However, they demonstrate the ability to render non-html templates (namely
  **Simple Event List** and **Year by Week** will return TeX source code),
  provide layout-specific configuration forms (**Lineatur**) or go beyond the
  simple listing of event instances (**Year by Week**).


.. _calingen-admin-doc-compilers-label:

*******************
Providing Compilers
*******************

What is a Compiler?
===================

|calingen| uses *compilers* to convert the result of the rendering process of
a layout into something usable (or - most likely - printable).

.. note::
  The original development idea of |calingen| was to generate TeX-templates of
  the calendar inlays and then use a TeX compiler (e.g. ``pdflatex``) to turn
  them into PDFs, ready for printing.

  However, during development, the focus on TeX was dropped in favour of a
  more generic approach, allowing
  :ref:`layouts <calingen-admin-doc-layouts-label>` to return any text-based
  result.

Technically, *compilers* are implementations of the app's plugin mount point
:class:`~calingen.interfaces.plugin_api.CompilerProvider`. They are resposible
for providing a valid HTTP response during the generation process (see
:ref:`calingen-dev-doc-plugins-compilerprovider-label` for implementation
details).

**How** this response is determined and **what** the actual response is, is up
to the respective compiler implementations, i.e. a compiler could accept
TeX-based layout outputs and run them through an actual TeX compiler, providing
the compilation result as an HTTP file download.


Integration of Compilers into the Project
=========================================

*Compilers* are **not required** to be Django applications. They are
dynamically imported while running the generation process of |calingen|.

This means they **must be importable**. This is the only requirement regarding
compilers.

.. note::
  *Compilers* will be imported by their full dotted Python path using Django's
  :func:`import_string function <django.utils.module_loading.import_string>`
  (see :class:`~calingen.views.generation.CompilerView` for implementation
  details).

Compilers may be provided as source code (i.e. by a GitHub repository) or as an
actual installable Python package (i.e. provided using `PyPI`_). If you want to
include third party compilers, make sure to follow their specific installation
instructions.

Obviously, there is a close connection between layouts and compilers. All
layouts indicate the type of their *rendered output* with their ``layout_type``
attribute.


Configuration
-------------

The app-specific setting :attr:`~calingen.settings.CALINGEN_COMPILER` is used
to determine, which layout will be processed by a given compiler.

Please refer to :attr:`~calingen.settings.CALINGEN_COMPILER` for details on
this setting and accepted values.


Thoughts on ``"default"`` Compilers
-----------------------------------

It is highly recommended to provide a *compiler* implementation as
``"default"`` in :attr:`~calingen.settings.CALINGEN_COMPILER` that is capable
of dealing with any type of layout.

This means, that compiler will most likely not perform ``layout_type``-specific
actions (e.g. launching a TeX compiler like ``pdflatex``), but process the
provided rendering result in some other way to create a valid HTTP response.

.. note::
  The project's administrator is in full control of the provided layouts and
  the included compilers. It is easily achievable to
  *just select the right compiler* and use that one as ``"default"``. But on
  the other hand, this might lead to problems on the long run.

  By providing a ``"default"`` compiler, that can handle any type of layout
  and then explicitly specifying specialized compilers, this is mitigated,
  keeping the project easily extendable.


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
