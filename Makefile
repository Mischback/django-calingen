# SPDX-License-Identifier: MIT

# This Makefile is not really a build tool. It provides shortcuts to run certain
# tasks while developing the application and serves as a convenient way to
# launch different tools with sane default settings.
#
# Actually, some of "make"'s capabilities is used to make sure that the
# tox environments, which are used to run most of the commands, are rebuild, if
# environment specifc configuration or requirements have changed.
#
# The Makefile is self-documenting, using code from here:
# https://gist.github.com/klmr/575726c7e05d8780505a#gistcomment-3586983
# The actual implementation is right at the bottom of this file and should be
# left untouched.

# ### INTERNAL SETTINGS / CONSTANTS
TOX_WORK_DIR := .tox
TOX_DJANGO_ENV := $(TOX_WORK_DIR)/django
TOX_SPHINX_ENV := $(TOX_WORK_DIR)/sphinx
TOX_UTIL_ENV := $(TOX_WORK_DIR)/util
TOX_TEST_ENV := $(TOX_WORK_DIR)/testing

DEVELOPMENT_REQUIREMENTS := requirements/common.txt requirements/coverage.txt requirements/development.txt
DOCUMENTATION_REQUIREMENTS := requirements/common.txt requirements/documentation.txt docs/source/conf.py
UTIL_REQUIREMENTS := requirements/coverage.txt requirements/util.txt


# some make settings
.SILENT :
.DELETE_ON_ERROR :
.DEFAULT_GOAL := help
MAKEFLAGS += --no-print-directory
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules


## Shortcut
## @category Development
run: django/runserver
.PHONY : run

## Shortcut
## @category Development
doc: sphinx/serve/html
.PHONY : doc


## Verify that the packaged app can be installed; used during CI only
## @category CI
ci/test/installation :
	tox -q -e installation
.PHONY : ci/test/installation

## Run a special test command on CI that tests the TeX-based layouts; used
## during CI only
## @category CI
ci/test/texlayoutcompilation :
	$(MAKE) dev/test test_command="-t requires_system_tex"
.PHONY : ci/test/texlayoutcompilation


## Remove temporary files
## @category Utility
clean : $(TOX_UTIL_ENV)
	- tox -q -e util -- coverage erase
	rm -rf docs/build/*
	rm -rf tmp_compilation
	rm -rf dist
	find . -iname "*.pyc" -delete
	find . -iname "__pycache__" -delete
	find . -iname ".coverage.*" -delete
.PHONY : clean

## Run tests to collect and show coverage information
## @category Development
dev/coverage : clean dev/test $(TOX_UTIL_ENV)
	- tox -q -e util -- coverage combine
	tox -q -e util -- coverage report
.PHONY : dev/coverage

test_command ?= ""
## Run the test suite
## @category Development
dev/test : $(TOX_TEST_ENV)
	tox -q -e testing -- $(test_command)
.PHONY : dev/test

test_tag ?= "current"
## Run only tests with a specific tag ("current" by default)
## @category Development
dev/test/tag :
	$(MAKE) dev/test test_command="-t $(test_tag)"
.PHONY : dev/test/tag


# ### Django management commands

django_command ?= "version"
django : $(TOX_DJANGO_ENV)
	tox -q -e django -- $(django_command)
.PHONY : django

## "$ django-admin check"; runs the project's checks
## @category Django
django/check :
	$(MAKE) django django_command="check"
.PHONY : django/check

## "$ django-admin clearsessions"; clears the session from the backend
## @category Django
django/clearsessions :
	$(MAKE) django django_command="clearsessions"
.PHONY : django/clearsessions

## "$ django-admin compilemessages"; compiles the app's *.po files to *.mo
## @category Django
django/compilemessages :
	$(MAKE) django django_command="compilemessages --ignore=.tox --ignore=tests --ignore=docs"
.PHONY : django/compilemessages

## create a superuser account with username: "admin" and password: "foobar"
## @category Django
django/createsuperuser :
	tox -q -e djangosuperuser
.PHONY : django/createsuperuser

## "$ django-admin makemessages"; collect the app's localizable strings into *.po
## @category Django
django/makemessages :
	$(MAKE) django django_command="makemessages --locale=en --locale=de --ignore=.tox --ignore=tests --ignore=docs"
.PHONY : django/makemessages

# Create the migrations for the app to be developed!
# TODO: The app name is hardcoded here!
## "$ django-admin makemigrations"; create migrations
## @category Django
django/makemigrations :
	$(MAKE) django django_command="makemigrations calingen"
.PHONY : django/makemigrations

## "$ django-admin migrate"; apply the project's migrations
## @category Django
django/migrate :
	$(MAKE) django django_command="migrate"
.PHONY : django/migrate

host_port ?= "0:8000"
## "django-admin runserver"; runs Django's development server with host = "0"
## and port = "8000".
## Host and port might be specified by "make django/runserver host_port="0:4444"
## to run the server on port "4444".
## @category Django
django/runserver : django/migrate django/clearsessions
	$(MAKE) django django_command="runserver $(host_port)"
.PHONY : django/runserver

## "django-admin shell"; run a REPL with the project's settings
## @category Django
django/shell :
	$(MAKE) django django_command="shell"
.PHONY : django/shell


# ### utility targets

## Run bandit on all files (*.py)
## @category Code Quality
util/bandit :
	$(MAKE) util/pre-commit pre-commit_id="bandit" pre-commit_files="--all-files"
.PHONY : util/bandit

## Run black on all files (*.py)
## @category Code Quality
util/black :
	$(MAKE) util/pre-commit pre-commit_id="black" pre-commit_files="--all-files"
.PHONY : util/black

## Run djlint on all files (*.html)
## @category Code Quality
util/djlint :
	$(MAKE) util/pre-commit pre-commit_id="djlint-django" pre-commit_files="--all-files"
.PHONY : util/djlint

## Run doc8 on all files (*.rst)
## @category Code Quality
util/doc8 :
	$(MAKE) util/pre-commit pre-commit_id="doc8" pre-commit_files="--all-files"
.PHONY : util/doc8

## Run flake8 on all files (*.py)
## @category Code Quality
util/flake8 :
	$(MAKE) util/pre-commit pre-commit_id="flake8" pre-commit_files="--all-files"
.PHONY : util/flake8

## Run isort on all files (*.py)
## @category Code Quality
util/isort :
	$(MAKE) util/pre-commit pre-commit_id="isort" pre-commit_files="--all-files"
.PHONY : util/isort

pre-commit_id ?= ""
pre-commit_files ?= ""
## Run all code quality tools as defined in .pre-commit-config.yaml
## @category Code Quality
util/pre-commit : $(TOX_UTIL_ENV)
	tox -q -e util -- pre-commit run $(pre-commit_files) $(pre-commit_id)
.PHONY : util/pre-commit

## Install pre-commit hooks to be executed automatically
## @category Code Quality
util/pre-commit/install : $(TOX_UTIL_ENV)
	tox -q -e util -- pre-commit install
.PHONY : util/pre-commit/install

## Update pre-commit hooks
## @category Code Quality
util/pre-commit/update : $(TOX_UTIL_ENV)
	tox -q -e util -- pre-commit autoupdate
.PHONY : util/pre-commit/update

flit_argument ?= "--version"
util/flit : $(TOX_UTIL_ENV)
	tox -q -e util -- flit $(flit_argument)
.PHONY : util/flit

## Use "flit" to build a PyPI-compatible package
## @category Utility
util/flit/build :
	$(MAKE) util/flit flit_argument="build"
.PHONY : util/flit/build

## Use "flit" to publish the package to PyPI
## @category Utility
util/flit/publish :
	$(MAKE) util/flit flit_argument="publish"
.PHONY : util/flit/publish

util/tox : $(TOX_DJANGO_ENV) $(TOX_SPHINX_ENV) $(TOX_TEST_ENV) $(TOX_UTIL_ENV)
.PHONY : util/tox


# ### Sphinx-related commands

## Build the documentation using "Sphinx"
## @category Development
sphinx/build/html : $(TOX_SPHINX_ENV)
	tox -q -e sphinx
.PHONY : sphinx/build/html

## Serve the documentation locally on port 8082
## @category Development
sphinx/serve/html : sphinx/build/html
	tox -q -e sphinx-serve
.PHONY : sphinx/serve/html


# ### INTERNAL RECIPES
$(TOX_DJANGO_ENV) : $(DEVELOPMENT_REQUIREMENTS) pyproject.toml
	tox --recreate -e django

$(TOX_SPHINX_ENV) : $(DOCUMENTATION_REQUIREMENTS) pyproject.toml
	tox --recreate -e sphinx

$(TOX_TEST_ENV) : $(DEVELOPMENT_REQUIREMENTS) pyproject.toml
	tox --recreate -e testing

$(TOX_UTIL_ENV) : $(UTIL_REQUIREMENTS) pyproject.toml .pre-commit-config.yaml
	tox --recreate -e util


# fancy colors
RULE_COLOR := "$$(tput setaf 6)"
VARIABLE_COLOR = "$$(tput setaf 2)"
VALUE_COLOR = "$$(tput setaf 1)"
CLEAR_STYLE := "$$(tput sgr0)"
TARGET_STYLED_HELP_NAME = "$(RULE_COLOR)TARGET$(CLEAR_STYLE)"
ARGUMENTS_HELP_NAME = "$(VARIABLE_COLOR)ARGUMENT$(CLEAR_STYLE)=$(VALUE_COLOR)VALUE$(CLEAR_STYLE)"

# search regex
target_regex = [a-zA-Z0-9%_\/%-]+
variable_regex = [^:=\s ]+
variable_assignment_regex = \s*:?[+:!\?]?=\s*
value_regex = .*
category_annotation_regex = @category\s+
category_regex = [^<]+

# tags used to delimit each parts
target_tag_start = "\<target-definition\>"
target_tag_end = "\<\\\/target-definition\>"
target_variable_tag_start = "\<target-variable\>"
target_variable_tag_end = "\<\\\/target-variable\>"
variable_tag_start = "\<variable\>"
variable_tag_end = "\<\\\/variable\>"
global_variable_tag_start = "\<global-variable\>"
global_variable_tag_end = "\<\\\/global-variable\>"
value_tag_start = "\<value\>"
value_tag_end = "\<\\\/value\>"
prerequisites_tag_start = "\<prerequisites\>"
prerequisites_tag_end = "\<\\\/prerequisites\>"
doc_tag_start = "\<doc\>"
doc_tag_end = "\<\\\/doc\>"
category_tag_start = "\<category-other\>"
category_tag_end = "\<\\\/category-other\>"
default_category_tag_start = "\<category-default\>"
default_category_tag_end = "\<\\\/category-default\>"

DEFAULT_CATEGORY = Targets and Arguments

## Show this help
help:
	@echo "Usage: make [$(TARGET_STYLED_HELP_NAME) [$(TARGET_STYLED_HELP_NAME) ...]] [$(ARGUMENTS_HELP_NAME) [$(ARGUMENTS_HELP_NAME) ...]]"
	@sed -n -e "/^## / { \
		h; \
		s/.*/##/; \
		:doc" \
		-E -e "H; \
		n; \
		s/^##\s*(.*)/$(doc_tag_start)\1$(doc_tag_end)/; \
		t doc" \
		-e "s/\s*#[^#].*//; " \
		-E -e "s/^(define\s*)?($(variable_regex))$(variable_assignment_regex)($(value_regex))/$(global_variable_tag_start)\2$(global_variable_tag_end)$(value_tag_start)\3$(value_tag_end)/;" \
		-E -e "s/^($(target_regex))\s*:?:\s*(($(variable_regex))$(variable_assignment_regex)($(value_regex)))/$(target_variable_tag_start)\1$(target_variable_tag_end)$(variable_tag_start)\3$(variable_tag_end)$(value_tag_start)\4$(value_tag_end)/;" \
		-E -e "s/^($(target_regex))\s*:?:\s*($(target_regex)(\s*$(target_regex))*)?/$(target_tag_start)\1$(target_tag_end)$(prerequisites_tag_start)\2$(prerequisites_tag_end)/;" \
		-E -e " \
		G; \
		s/##\s*(.*)\s*##/$(doc_tag_start)\1$(doc_tag_end)/; \
		s/\\n//g;" \
		-E -e "/$(category_annotation_regex)/!s/.*/$(default_category_tag_start)$(DEFAULT_CATEGORY)$(default_category_tag_end)&/" \
		-E -e "s/^(.*)$(doc_tag_start)$(category_annotation_regex)($(category_regex))$(doc_tag_end)/$(category_tag_start)\2$(category_tag_end)\1/" \
		-e "p; \
	}"  ${MAKEFILE_LIST} \
	| sort  \
	| sed -n \
		-e "s/$(default_category_tag_start)/$(category_tag_start)/" \
		-e "s/$(default_category_tag_end)/$(category_tag_end)/" \
		-E -e "{G; s/($(category_tag_start)$(category_regex)$(category_tag_end))(.*)\n\1/\2/; s/\n.*//; H; }" \
		-e "s/$(category_tag_start)//" \
		-e "s/$(category_tag_end)/:\n/" \
		-e "s/$(target_variable_tag_start)/$(target_tag_start)/" \
		-e "s/$(target_variable_tag_end)/$(target_tag_end)/" \
		-e "s/$(target_tag_start)/    $(RULE_COLOR)/" \
		-e "s/$(target_tag_end)/$(CLEAR_STYLE) /" \
		-e "s/$(prerequisites_tag_start)$(prerequisites_tag_end)//" \
		-e "s/$(prerequisites_tag_start)/[/" \
		-e "s/$(prerequisites_tag_end)/]/" \
		-E -e "s/$(variable_tag_start)/$(VARIABLE_COLOR)/g" \
		-E -e "s/$(variable_tag_end)/$(CLEAR_STYLE)/" \
		-E -e "s/$(global_variable_tag_start)/    $(VARIABLE_COLOR)/g" \
		-E -e "s/$(global_variable_tag_end)/$(CLEAR_STYLE)/" \
		-e "s/$(value_tag_start)/ (default: $(VALUE_COLOR)/" \
		-e "s/$(value_tag_end)/$(CLEAR_STYLE))/" \
		-e "s/$(doc_tag_start)/\n        /g" \
		-e "s/$(doc_tag_end)//g" \
		-e "p"
.PHONY : help
