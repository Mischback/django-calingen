# This Makefile is not really a build tool. It provides shortcuts to run certain
# tasks while developing the application and serves as a convenient way to
# launch different tools with sane default settings.

# some make settings
.SILENT :
.DELETE_ON_ERROR :
MAKEFLAGS += --no-print-directory
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

# ### Django management commands

django_command ?= "version"
django :
	tox -q -e django -- $(django_command)
.PHONY : django

django/check :
	$(MAKE) django django_command="check"
.PHONY : django/check

django/migrate :
	$(MAKE) django django_command="migrate"
.PHONY : django/migrate

host_port ?= "0:8000"
django/runserver : django/migrate
	$(MAKE) django django_command="runserver $(host_port)"
.PHONY : django/runserver

django/shell :
	$(MAKE) django django_command="shell"
.PHONY : django/shell

# ### utility targets

util/bandit :
	$(MAKE) util/pre-commit pre-commit_id="bandit"
.PHONY : util/bandit

util/black :
	$(MAKE) util/pre-commit pre-commit_id="black"
.PHONY : util/black

util/flake8 :
	$(MAKE) util/pre-commit pre-commit_id="flake8"
.PHONY : util/flake8

util/isort :
	$(MAKE) util/pre-commit pre-commit_id="isort"
.PHONY : util/isort

util/mypy :
	$(MAKE) util/pre-commit pre-commit_id="mypy"
.PHONY : util/mypy

pre-commit_id ?= ""
util/pre-commit :
	tox -q -e util -- pre-commit run $(pre-commit_id)
.PHONY : util/pre-commit
