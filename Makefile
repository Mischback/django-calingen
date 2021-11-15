# This Makefile is not really a build tool. It provides shortcuts to run certain
# tasks while developing the application and serves as a convenient way to
# launch different tools with sane default settings.

# some make settings
.SILENT :
.DELETE_ON_ERROR :
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

# ### utility targets

util/black :
	$(MAKE) util/pre-commit pre-commit_id="black"
.PHONY : util/black

pre-commit_id ?= ""
util/pre-commit :
	tox -q -e util -- pre-commit run $(pre-commit_id)
.PHONY : util/pre-commit
