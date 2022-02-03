.. _calingen-cookbook-setup-step-by-step-label:

##########################
Setup Guide (Step by Step)
##########################

This recipe describes the setup of |calingen| from scratch. In includes
installation and configuration of the app in a fresh Django project.

It is by no means a guide on how to setup a *production-ready* Django project,
which is a feat of science and/or magic by itsself. However, following this
recipe will result in a working installation of Django with |calingen| and
may provide reference on how to integrate |calingen| with an existing Django
project or provide the starting point to an actual *production-ready* Django
project.

.. note::
  This recipe describes the installation on a Linux host. Commands on Windows
  or MacOS hosts may vary, but there is little to none interaction with the
  actual operating system, so this guide should be applicable to all hosts.

.. warning::
  Though not explicitly mentioned in the following step-by-step guide, it is
  considered best practice to separate Python-related projects using *virtual
  environments*.

  There are several solutions for creating and managing these virtual
  environments, but for a quick start, just follow
  `this tutorial on the venv module <https://docs.python.org/3/tutorial/venv.html>`_
  to get started.

To verify that the hosts provides at least Python 3.7, just run: ::

  ~ $ python --version
  Python 3.9.2


********************
Django Project Setup
********************


Django Installation
===================

As this is a step-by-step guide, the very first step is to install Django and
create an actual project.

.. note::
  The difference of Django *projects* and *applications (apps)* might be
  confusing at first.
  `Here's a relevant SO question <https://stackoverflow.com/questions/19350785/what-s-the-difference-between-a-project-and-an-app-in-django-world>`_
  and |here is a relevant section from the Django documentation|.

To install Django, just run: ::

  ~ $ pip install django
  Collecting django
    Downloading Django-4.0.2-py3-none-any.whl (8.0 MB)
  Collecting asgiref<4,>=3.4.1
    Using cached asgiref-3.5.0-py3-none-any.whl (22 kB)
  Collecting sqlparse>=0.2.2
    Using cached sqlparse-0.4.2-py3-none-any.whl (42 kB)
  Installing collected packages: sqlparse, asgiref, django
  Successfully installed asgiref-3.5.0 django-4.0.2 sqlparse-0.4.2

After the installation of Django, the ``django-admin`` command should be
available on your command line. This built-in utility is used to create the
actual *project*. It will create the required directory and file structure
of a project, including a default ``settings`` module. ::

  ~ $ django-admin startproject cookbook

  ~ $ cd cookbook

  ~/cookbook $ tree
  .
  ├── cookbook
  │   ├── asgi.py
  │   ├── __init__.py
  │   ├── settings.py
  │   ├── urls.py
  │   └── wsgi.py
  └── manage.py

  1 directory, 6 files

.. note::
  The command sequence above creates a project with the name ``cookbook``. Most
  likely you will want to name your own project differently. Just keep that in
  mind and adapt the following commands accordingly.

Verify the installation is working with the following commands: ::

  ~/cookbook $ ./manage.py migrate
  Operations to perform:
    Apply all migrations: admin, auth, contenttypes, sessions
  Running migrations:
    Applying contenttypes.0001_initial... OK
    Applying auth.0001_initial... OK
    Applying admin.0001_initial... OK
    Applying admin.0002_logentry_remove_auto_add... OK
    Applying admin.0003_logentry_add_action_flag_choices... OK
    Applying contenttypes.0002_remove_content_type_name... OK
    Applying auth.0002_alter_permission_name_max_length... OK
    Applying auth.0003_alter_user_email_max_length... OK
    Applying auth.0004_alter_user_username_opts... OK
    Applying auth.0005_alter_user_last_login_null... OK
    Applying auth.0006_require_contenttypes_0002... OK
    Applying auth.0007_alter_validators_add_error_messages... OK
    Applying auth.0008_alter_user_username_max_length... OK
    Applying auth.0009_alter_user_last_name_max_length... OK
    Applying auth.0010_alter_group_name_max_length... OK
    Applying auth.0011_update_proxy_permissions... OK
    Applying auth.0012_alter_user_first_name_max_length... OK
    Applying sessions.0001_initial... OK

  ~/cookbook $ ./manage.py runserver
  Watching for file changes with StatReloader
  Performing system checks...

  System check identified no issues (0 silenced).
  February 01, 2022 - 09:26:04
  Django version 4.0.2, using settings 'cookbook.settings'
  Starting development server at http://127.0.0.1:8000/
  Quit the server with CONTROL-C.

This has started Django's internal development server on port ``8000``. Verify
that the installation was successful by visiting ``http://127.0.0.1:8000`` with
your browser and then terminate the server again by pressing ``CONTROL-c``.


Create a Superuser
==================

To make your Django project administrable from the web interface, a superuser
account is required: ::

  ~/cookbook $ ./manage.py createsuperuser

This will prompt for username, email and password. Fill and proceed.


Enable Authentication
=====================

Out of the box, Django already provides the required views to authenticate
users. However, these are not activated by default (see
|Authentication Views in Django's documentation| for details).

First of all, include the required urls in the project's *url configuration*
by editing ``~/cookbook/cookbook/urls.py``: ::

  from django.contrib import admin
  from django.urls import include, path  # <- make sure to import "include"

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('accounts/', include('django.contrib.auth.urls')),  # <- added!
  ]

To make these views work, they require corresponding templates. The project
configuration must be updated by adjusting the :setting:`TEMPLATES` in
``~/cookbook/cookbook/settings.py``: ::

  TEMPLATES = [
      {
          'BACKEND': 'django.template.backends.django.DjangoTemplates',
          'DIRS': [
              BASE_DIR / 'templates',  # <- add a project-specific directory
          ],
          'APP_DIRS': True,
          'OPTIONS': {
              'context_processors': [
                  'django.template.context_processors.debug',
                  'django.template.context_processors.request',
                  'django.contrib.auth.context_processors.auth',
                  'django.contrib.messages.context_processors.messages',
              ],
          },
      },
  ]

The setting must be transfered to an actual directory on the filesystem: ::

  ~/cookbook $ mkdir templates

To make the *login* work, at least the template for the ``LoginView`` has to be
provided. |Django's documentation has a list of the assumed template names|,
which is ``"registration/login.html"`` for the ``LoginView``.

Create a file ``~/cookbook/templates/registration/login.html`` with the
following content: ::

  <!DOCTYPE html>
  <html lang="en">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Login</title>
    </head>
    <body>
      <h1>Login</h1>
      <form method="post">
      {% csrf_token %}
      {{ form.as_p }}
      <button type="submit">Login</button>
      </form>
    </body>
  </html>

.. note::
  The HTML snippet is just a minimal login template. It can be refined by the
  specific needs of the project. It is intended as a *starting point*.

  If you're integrating |calingen| into an existing Django project, most likely
  you will already have a working login/logout solution.



**************
Calingen Setup
**************

App Installation
================

|calingen| is installable from `PyPI <https://pypi.org>`_: ::

  ~/cookbook $ pip install django-calingen
  Successfully installed django-calingen-0.0.2 python-dateutil-2.8.2 six-1.10.0

Ok, the required packages should have been installed by now. Let's move to the
configuration.


Integration into the Project
============================

Open the project's ``settings`` module (``~/cookbook/cookbook/settings.py``)
and modify the :setting:`INSTALLED_APPS` like this: ::

  INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'calingen',  # <- added!
  ]

Now apply the app-specific database migrations by running ::

  ~/cookbook $ ./manage.py migrate

Include the app-specific urls in the project's *url configuration* (
``~/cookbook/cookbook/urls.py``): ::

  from django.contrib import admin
  from django.urls import include, path

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('accounts/', include('django.contrib.auth.urls')),
      path('calingen/', include('calingen.urls')),  # <- added!
  ]

External Events, Layouts and Compilers
======================================

Besides the actual app |calingen|, it is required to set up
:ref:`compilers <calingen-cookbook-ingredients-compilers-label>`,
:ref:`layouts <calingen-cookbook-ingredients-layouts-label>` and -
*optionally* -
:ref:`external events <calingen-cookbook-ingredients-eventprovider-label>`.

.. warning::
  TODO: create a dedicated document that describes the role of layouts,
  compilers and event providers and how these three components interact.

  This is not identical to
  :ref:`calingen-dev-doc-layout-rendering-compilation-label`

.. warning::
  TODO: When :issue:`49` is closed, provide an example listing of the recipe's
  ``INSTALLED_APPS`` with one layout and one event provider included.

.. note::
  How :ref:`compilers <calingen-cookbook-ingredients-compilers-label>` can be
  integrated in the project is described in the following section
  :ref:`calingen-cookbook-setup-step-by-step-compiler-mapping-label`.


.. _calingen-cookbook-setup-step-by-step-settings:

App-specific Settings
=====================

|calingen| has some app-specific settings that may be adjusted using the
project's ``settings`` module. A thorough description of these settings can be
found in :mod:`calingen.settings`' documentation.

.. warning::
  :attr:`calingen.settings.CALINGEN_EXTERNAL_EVENT_PROVIDER` is not described
  here, because this setting will be removed; see :issue:`49`.


.. _calingen-cookbook-setup-step-by-step-compiler-mapping-label:

Map Layouts to Compilers
------------------------

Depending on the layouts that should be provided, the
:attr:`~calingen.settings.CALINGEN_COMPILER` setting needs adjustment. Simply
include the setting in the project's ``settings`` module (
``~/cookbook/cookbook/settings.py``).

As described :ref:`here <calingen-cookbook-ingredients-compilers-label>`,
|calingen| ships with three compilers ready to be used. For demonstration
purposes, a corresponding example configuration is provided: ::

  CALINGEN_COMPILER = {
    'default': 'calingen.contrib.compilers.html_or_download.compiler.HtmlOrDownloadCompiler',
    'tex':'calingen.contrib.compilers.copy_paste.compiler.CopyPasteCompiler',
  }

This will establish the ``HtmlOrDownloadCompiler`` as the *default one*, but
use ``CopyPasteCompiler`` for layouts that render to TeX sources.

This will make using ``SimpleEventList`` result in the TeX sources be provided
in an HTML output, ready to be copy and pasted, while the results of using
``Lineatur`` are directly displayed in the browser window.

.. important::
  It is highly recommended to provide a *compiler* implementation as
  ``"default"`` in :attr:`~calingen.settings.CALINGEN_COMPILER` that is capable
  of dealing with any type of layout.

  This means, that compiler will most likely not perform
  ``layout_type``-specific actions (e.g. launching a TeX compiler like
  ``pdflatex``), but process the provided rendering result in some other way to
  create a valid HTTP response.


.. |here is a relevant section from the Django documentation| replace:: :djangoapi:`here is a relevant section from the Django documentation <applications/#projects-and-applications>`
.. |Authentication Views in Django's documentation| replace:: :djangodoc:`Authentication Views in Django's documentation <topics/auth/default/#module-django.contrib.auth.views>`
.. |Django's documentation has a list of the assumed template names| replace:: :djangodoc:`Django's documentation has a list of the assumed template names <topics/auth/default/#all-authentication-views>`
.. |calingen| replace:: **django-calingen**
