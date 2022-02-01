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


************
Installation
************

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


App Installation
================





.. |here is a relevant section from the Django documentation| replace:: :djangoapi:`here is a relevant section from the Django documentation <applications/#projects-and-applications>`
.. |calingen| replace:: **django-calingen**
