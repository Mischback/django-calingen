# SPDX-License-Identifier: MIT

# This Makefile is not really a build tool. It provides shortcuts to run certain
# tasks while developing the application and serves as a convenient way to
# launch different tools with sane default settings.

# ### INTERNAL SETTINGS / CONSTANTS
TOX_WORK_DIR := .tox
TOX_DJANGO_ENV := $(TOX_WORK_DIR)/django
TOX_SPHINX_ENV := $(TOX_WORK_DIR)/sphinx
TOX_UTIL_ENV := $(TOX_WORK_DIR)/util
TOX_TEST_DIR := $(TOX_WORK_DIR)/testing

DEVELOPMENT_REQUIREMENTS := requirements/common.txt requirements/coverage.txt requirements/development.txt
DOCUMENTATION_REQUIREMENTS := requirements/common.txt requirements/documentation.txt
UTIL_REQUIREMENTS := requirements/coverage.txt requirements/util.txt


# some make settings
.SILENT :
.DELETE_ON_ERROR :
MAKEFLAGS += --no-print-directory
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules


run: django/runserver
.PHONY : run

doc: sphinx/serve/html
.PHONY : doc


ci/test/texlayoutcompilation :
	$(MAKE) dev/test test_command="-t requires_system_tex"
.PHONY : ci/test/texlayoutcompilation


clean : $(TOX_UTIL_ENV)
	- tox -q -e util -- coverage erase
	rm -rf docs/build/*
	rm -rf tmp_compilation
	find . -iname "*.pyc" -delete
	find . -iname "__pycache__" -delete
	find . -iname ".coverage.*" -delete
.PHONY : clean

dev/coverage : clean dev/test $(TOX_UTIL_ENV)
	- tox -q -e util -- coverage combine
	tox -q -e util -- coverage report
.PHONY : dev/coverage

test_command ?= ""
dev/test : $(TOX_TEST_DIR)
	tox -q -e testing -- $(test_command)
.PHONY : dev/test

test_tag ?= "current"
dev/test/tag :
	$(MAKE) dev/test test_command="-t $(test_tag)"
.PHONY : dev/test/tag


# ### Django management commands

django_command ?= "version"
django : $(TOX_DJANGO_ENV)
	tox -q -e django -- $(django_command)
.PHONY : django

django/check :
	$(MAKE) django django_command="check"
.PHONY : django/check

django/clearsessions :
	$(MAKE) django django_command="clearsessions"
.PHONY : django/clearsessions

django/compilemessages :
	$(MAKE) django django_command="compilemessages --ignore=.tox --ignore=tests --ignore=docs"
.PHONY : django/compilemessages

django/createsuperuser :
	tox -q -e djangosuperuser
.PHONY : django/createsuperuser

django/makemessages :
	$(MAKE) django django_command="makemessages --locale=en --locale=de --ignore=.tox --ignore=tests --ignore=docs"
.PHONY : django/makemessages

# Create the migrations for the app to be developed!
# TODO: The app name is hardcoded here!
django/makemigrations :
	$(MAKE) django django_command="makemigrations calingen"
.PHONY : django/makemigrations

django/migrate :
	$(MAKE) django django_command="migrate"
.PHONY : django/migrate

host_port ?= "0:8000"
django/runserver : django/migrate django/clearsessions
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

util/djlint :
	$(MAKE) util/pre-commit pre-commit_id="djlint-django" pre-commit_files="--all-files"
.PHONY : util/djlint

util/flake8 :
	$(MAKE) util/pre-commit pre-commit_id="flake8" pre-commit_files="--all-files"
.PHONY : util/flake8

util/isort :
	$(MAKE) util/pre-commit pre-commit_id="isort" pre-commit_files="--all-files"
.PHONY : util/isort

pre-commit_id ?= ""
pre-commit_files ?= ""
util/pre-commit : $(TOX_UTIL_ENV)
	tox -q -e util -- pre-commit run $(pre-commit_files) $(pre-commit_id)
.PHONY : util/pre-commit

util/pre-commit/install : $(TOX_UTIL_ENV)
	tox -q -e util -- pre-commit install
.PHONY : util/pre-commit/install

util/pre-commit/update : $(TOX_UTIL_ENV)
	tox -q -e util -- pre-commit autoupdate
.PHONY : util/pre-commit/update

flit_argument ?= "--version"
util/flit : $(TOX_UTIL_ENV)
	tox -q -e util -- flit $(flit_argument)
.PHONY : util/flit

util/tox : $(TOX_DJANGO_ENV) $(TOX_SPHINX_ENV) $(TOX_TEST_DIR) $(TOX_UTIL_ENV)
.PHONY : util/tox


# ### Sphinx-related commands

sphinx/build/html : $(TOX_SPHINX_ENV)
	tox -q -e sphinx
.PHONY : sphinx/build/html

sphinx/serve/html : sphinx/build/html
	tox -q -e sphinx-serve
.PHONY : sphinx/serve/html


# ### INTERNAL RECIPES
$(TOX_DJANGO_ENV) : $(DEVELOPMENT_REQUIREMENTS) pyproject.toml
	tox --recreate -e django

$(TOX_SPHINX_ENV) : $(DOCUMENTATION_REQUIREMENTS) pyproject.toml
	tox --recreate -e sphinx

$(TOX_TEST_DIR) : $(DEVELOPMENT_REQUIREMENTS) pyproject.toml
	tox --recreate -e testing

$(TOX_UTIL_ENV) : $(UTIL_REQUIREMENTS) pyproject.toml .pre-commit-config.yaml
	tox --recreate -e util
