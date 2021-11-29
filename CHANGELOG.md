# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- provide _Github Action_-based Continuous Integration, running linters, tests
  and reporting coverage to coveralls.io
- provide code quality tools by _pre-commit_
- add model ``Event``, including views for _CRUD_
- add model ``Profile``, including views for _CRUD_
- add module ``interfaces``
  - add ``data_exchange`` interfaces, to pass calender entries or list of them
    between different components of the application
  - add a generic plugin api
  - add a plugin api to provide events
  - add a app-specific form field and widget to handle plugins



### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security
