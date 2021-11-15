# This Makefile is not really a build tool. It provides shortcuts to run certain
# tasks while developing the application and serves as a convenient way to
# launch different tools with sane default settings.

# some make settings
.SILENT :
.DELETE_ON_ERROR :
MAKEFLAGS += --no-print-directory
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

# ### utility targets

util/black :
	$(MAKE) util/pre-commit pre-commit_id="black"
.PHONY : util/black

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
