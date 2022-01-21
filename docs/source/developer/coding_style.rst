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

Python Docstrings
=================

************************
Additional Documentation
************************

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

  | *If applied, this commmit will* **your subject line here**

.. _How to write a Git Commit Message: https://chris.beams.io/posts/git-commit/

.. |calingen| replace:: **django-calingen**
