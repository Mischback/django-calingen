# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- provide _GitHub Action_-based Continuous Integration:
  - automatic running of code quality tools (linters)
  - automatic running of test suite including reporting to coveralls
  - automatic building of Python package using ``flit``
  - automatic releases to PyPI (for ``main`` branch)
- provide code quality tools by _pre-commit_ (see documentation for details)
- provide stand-alone development environment with only ``tox`` as dependency
- add model ``Event``, including views for _CRUD_
- add model ``Profile``, including views for _CRUD_
- provide a basic integration in Django's admin interface for app's models
- add ``data_exchange`` module to ``interfaces``, to pass calendar entries or
  lists of them between different components of the application
- add ``plugin_api`` module to ``interfaces`` with three possible interfaces to
  attach plugins to
  - ``EventProvider``: enable provision of (external) events
  - ``LayoutProvider``: enable inclusion of third-party layouts
  - ``CompilerProvider``: enable inclusion of third-party compilers
- implement ``EventProvider`` for German holidays
  (``contrib.providers.german_holidays``)
- implement three demonstration layouts (``contrib.layouts``):
  - ``lineatur``
  - ``simple_event_list``
  - ``year_by_week``
- implement three default compilers (``contrib.compiler``):
  - ``copy_paste``
  - ``download``
  - ``html_or_download``
- provide required ``Views`` to make the whole build process work
- provide custom templatetags ``calingen_escape`` to escape special characters
  during layout rendering process
- provide initial set of templates (these do work but are expected to be
  substituted in a real project)
- make the whole app localizable
  - in Python code, all strings are marked for translation
  - templates do not provide localization hooks (as they are expected to be
    substituted in a real project)
  - provide default translation for German
- provide app-specific contributions to Django's check framework (basically to
  check if the required configuration is met)
- provide an app-specific settings module to provide default values for the
  app's required configuration values
- loads of source code documentation (Numpy style)
- a set of documentation for users, administrators and developers


### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security
