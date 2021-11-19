# Contributing to _django-calingen_

First of all: **Thank you** for taking the time to contribute!


## How Can I Contribute?

### Bug Reports

You did encounter a bug? Or at least, something is not behaving like you had
expected? **Great!** Hunting down bugs and issues is actually hard!

Please submit bug reports using the project's
[Issue Tracker@github](https://github.com/Mischback/django-calingen/issues).


### Feature Requests / Enhancement Suggestions

You have a really awesome idea for a new function? Tell me about it!

Again, please submit using the project's
[Issue Tracker@github](https://github.com/Mischback/django-calingen/issues).


### Code Contribution

_Getting right to it, huh?_ Obviously, code contributions are welcome! You know
the deal: _fork_, _code_, _test_ and **create a pull request**.

Please see below to get you started, **django-calingen** is setup to make all
required (or at least recommended) tools available without too much effort.


## Easy Environment Setup for Developers

After cloning the repository you're nearly done in setting up your development
environment. The only development dependencies are actually ``tox`` and ``make``.

Everything else is handled by the project's ``pyproject.toml`` and ``Makefile``,
though it is highly recommended to run

```bash
$ make util/pre-commit/install
```

to activate ``pre-commit`` hooks as defined in ``.pre-commit-config.yaml``.
These hooks will ensure basic code quality by using tools like
[black](https://github.com/psf/black) and
[flake8](https://github.com/PyCQA/flake8).

However, these tools will also be run during the Continuous Integration (CI) on
any pull request and may cause the build to fail.

I highly recommend to have a look into the ``Makefile``, which serves as the
central command line interface during development. In example: several Django
commands are provided there.


### Code Style

- The Python source code is formatted using [black](https://github.com/psf/black);
  this basically means: You should not need to care about code formatting.
- As a guideline: aim to reuse as much of the Django framework as possible
  (that's the idea of using a framework, isn't it?).
- Testing is important! Cover your code with unit tests.
- Provide documentation for your code. [flake8](https://github.com/PyCQA/flake8)
  is configured to highlight missing documentation.


### Documentation Styleguide

- The documentation is generated using
  [Sphinx](https://github.com/sphinx-doc/sphinx); its configuration is provided
  in ``docs/source/conf.py``.
- The provided configuration expects its docstrings in _numpy style_ (see its
  documentation [here](https://developer.lsst.io/python/numpydoc.html)).


### Git Commit Message Styleguide

- highly recommended article:
  [How to write a Git Commit Message](https://chris.beams.io/posts/git-commit/)
- **tl;dr**:
  - Separate subject from body with one blank line
  - Limit the subject line to 50 characters
  - Capitalize the subject line
  - Do not end the subject line with a period
  - Use the imperative mood in the subject line
  - Wrap the body at around 72 characters
  - Use the body to explain _what_ and _why_ vs. _how_
- As a general guideline: the commit subject line should finish this sentence:
  _If applied, this commmit will_ **your subject line here**
