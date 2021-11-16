# SPDX-License-Identifier: MIT

# This Makefile is not really a build tool. It provides shortcuts to run certain
# tasks while developing the application and serves as a convenient way to
# launch different tools with sane default settings.

# some make settings
.SILENT :
.DELETE_ON_ERROR :
MAKEFLAGS += --no-print-directory
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules


clean :
	- tox -q -e util -- coverage erase
	rm -rf docs/build/*
	find . -iname "*.pyc" -delete
	find . -iname "__pycache__" -delete
	find . -iname ".coverage.*" -delete
.PHONY : clean

dev/coverage : clean dev/test
	- tox -q -e util -- coverage combine
	tox -q -e util -- coverage report
.PHONY : dev/coverage

test_command ?= ""
dev/test :
	tox -q -e testing -- $(test_command)
.PHONY : dev/test

test_tag ?= "current"
dev/test/tag :
	$(MAKE) dev/test test_command="-t $(test_tag)"
.PHONY : dev/test/tag


# ### Django management commands

django_command ?= "version"
django :
	tox -q -e django -- $(django_command)
.PHONY : django

django/check :
	$(MAKE) django django_command="check"
.PHONY : django/check

django/createsuperuser :
	tox -q -e djangosuperuser
.PHONY : django/createsuperuser

# Create the migrations for the app to be developed!
# TODO: The app name is hardcoded here!
django/makemigrations :
	$(MAKE) django django_command="makemigrations calingen"
.PHONY : django/makemigrations

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
	$(MAKE) util/pre-commit pre-commit_id="bandit" pre-commit_files="--all-files"
.PHONY : util/bandit

util/black :
	$(MAKE) util/pre-commit pre-commit_id="black" pre-commit_files="--all-files"
.PHONY : util/black

util/flake8 :
	$(MAKE) util/pre-commit pre-commit_id="flake8" pre-commit_files="--all-files"
.PHONY : util/flake8

util/isort :
	$(MAKE) util/pre-commit pre-commit_id="isort" pre-commit_files="--all-files"
.PHONY : util/isort

util/mypy :
	$(MAKE) util/pre-commit pre-commit_id="mypy" pre-commit_files="--all-files"
.PHONY : util/mypy

pre-commit_id ?= ""
pre-commit_files ?= ""
util/pre-commit :
	tox -q -e util -- pre-commit run $(pre-commit_files) $(pre-commit_id)
.PHONY : util/pre-commit

util/pre-commit/update :
	tox -q -e util -- pre-commit autoupdate
.PHONY : util/pre-commit/update


# ### Sphinx-related commands

sphinx/build/html :
	tox -q -e sphinx
.PHONY : sphinx/build/html

sphinx/serve/html : sphinx/build/html
	tox -q -e sphinx-serve
.PHONY : sphinx/serve/html
