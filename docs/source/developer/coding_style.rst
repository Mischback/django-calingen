############
Coding Style
############

The following sections describe the style conventions for all source code
inside of the repository.

They should be considered *guidelines*, you're free to do whatever you desire.
However, some of them are actually checked during CI, causing builds to fail.

If you activated ``pre-commit`` as per
:ref:`Getting Started <calingen-dev-doc-setup-getting-started-label>`, you
should be good to go!


******************
Python Source Code
******************

- The Python source code is formatted using `black`_; this basically means:
  You should not need to care about code formatting.
- As a guideline: aim to reuse as much of the Django framework as possible
  (that's the idea of using a framework, isn't it?).
- Testing is important! Cover your code with unit tests.
- Provide documentation for your code. `flake8`_ is configured to highlight
  missing documentation.

.. _black: https://github.com/psf/black
.. _flake8: https://github.com/PyCQA/flake8


*************
Documentation
*************

Documentation is generated using `Sphinx`_ and meant to be published on
`Read the Docs`_ (`django-calingen@RtD`_).

The configuration for ``Sphinx`` is provided in :source:`docs/source/conf.py`.

.. _Sphinx: https://github.com/sphinx-doc/sphinx
.. _Read the Docs: https://readthedocs.org/
.. _django-calingen@RtD: https://django-calingen.readthedocs.io/en/latest/


Python Docstrings
=================

The app's source code is documented with Python ``docstrings`` in
`Numpy Style`_.

.. note::
  The source code documentation may appear extensive. The actual idea is to
  have documentation available, that enables new contributors to quickly
  understand the purpose of classes and functions, so that they can build
  upon the existing code base.

  The actual benchmark for documentation is:

    | Do I understand the purpose of that item after several weeks without
    | working with the repository?

``Sphinx`` does pick up the docstrings to automatically generate an
:ref:`api/index:API Reference`. That reference is intended to be used by
developers and is referenced from this text documentation, if applicable.

Internally, ``Sphinx`` uses the plugin `sphinx-autoapi`_ in combination with
`napoleon`_ to generate the API reference.

.. _Numpy Style: https://developer.lsst.io/python/numpydoc.html
.. _sphinx-autoapi: https://github.com/readthedocs/sphinx-autoapi
.. _napoleon: https://github.com/sphinx-contrib/napoleon


Additionnal Available ``Sphinx`` Roles
--------------------------------------

Besides ``Sphinx``'s `pre-defined roles of the Python domain`_, the following
additional ``roles`` are provided through :source:`docs/source/conf.py`:

.. note::
  ``roles`` that resolve to Django's documentation are internally provided
  using ``intersphinx``. Beside the listed *additional roles* this works for
  ``Sphinx``'s pre-defined roles (i.e. ``:class:``) aswell.

  The referenced *version* of Django is automatically determined. Internally
  ``django`` is installed into
  :ref:`tox's sphinx environment <calingen-dev-doc-setup-desc-tox-env-label>`,
  with the version specified in :source:`requirements/common.txt`. The
  installed Django version will determine the version of the cross-referenced
  documentation.

  Details may be found in ``docs/source/conf.py``.

``:djangodoc:`` / ``:djangoapi:``
  Reference an object in :djangodoc:`Django's documentation </>`. The
  difference between these roles may be described as follows:

  Parts of :djangoapi:`Django's API </>` should be referenced by
  ``:djangoapi:``, while additional documents (i.e.
  :djangodoc:`like the tutorial <intro/tutorial01>`) should use
  ``:djangodoc:``.

``:setting:``
  Directly reference a :djangoapi:`Django setting <settings>`, e.g.::

    :setting:`INSTALLED_APPS`

  will generate a hyperlink like this: :setting:`INSTALLED_APPS`.

``:ttag:``
  Directly reference
  :djangoapi:`one of Django's included Template Tags <templates/builtins>`,
  e.g.::

    :ttag:`autoescape`

  will generate a hyperlink like this: :ttag:`autoescape`.

``:tfilter:``
  Directly reference
  :djangoapi:`one of Django's included Template Filters <templates/builtins>`,
  e.g.::

    :tfilter:`add`

  will generate a hyperlink like this: :tfilter:`add`.

``:commit:``
  Reference a commit of the
  `project's repo <https://github.com/Mischback/django-calingen>`_, e.g.::

    :commit:`fd5f533964e6b3555c559b9baae9f03314e98533`

  will generate a hyperlink like this
  :commit:`fd5f533964e6b3555c559b9baae9f03314e98533`.

  It is recommended to manually shorten the created link like this::

    :commit:`fd5f533 <fd5f533964e6b3555c559b9baae9f03314e98533>`

  resulting in :commit:`fd5f533 <fd5f533964e6b3555c559b9baae9f03314e98533>`.

``:issue:``
  Reference an issue in the
  `project's repo <https://github.com/Mischback/django-calingen>`_ by number,
  e.g.::

    :issue:`26`

  will generate a hyperlink like this: :issue:`26`.

``:source:``
  Reference a file or directory in the
  `project's repo <https://github.com/Mischback/django-calingen>`_, e.g.::

    :source:`docs/source/conf.py`

  will generate a hyperlink like this: :source:`docs/source/conf.py`.

  .. note::
    The file will be looked up in the repository's *default branch*, which is
    ``development``.

    Linking to directories works aswell, e.g. :source:`docs/source`.

.. _pre-defined roles of the Python domain: https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#python-roles


Additional text-based Documentation
===================================

The additional text-based documentation is provided as *reStructuredText* files
in :source:`docs/source`.

Three audiences should be considered when writing documentation:

- **Users** - Describe features and how they are meant to be used. Assume
  non-tech readers, so keep technical details out of this documents.

  See :ref:`calingen-user-doc-label`.
- **Administrators** - Describe features and how they are configured while
  deploying a Django project. Include technical details but don't dive into
  implementation details. While this audience can be assumed to have at least
  Python knowledge, they might not care for all the details.

  See :ref:`calingen-admin-doc-label`.
- **Developers** - Don't hide anything. This is the most thourough description
  of the app, including even small implementation details.

  Most likely these persons will rely on the :ref:`api/index:API Reference`
  generated from ``docstrings`` aswell as actually reading the source code with
  its *inline comments*. The *text-based documentation* might be used for
  providing additional context and generalized descriptions.

  This is, what you're reading just now.


*******************
Git Commit Messages
*******************

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

  | *If applied, this commmit will* **[your subject line here]**

.. _How to write a Git Commit Message: https://chris.beams.io/posts/git-commit/

.. |calingen| replace:: **django-calingen**
