PACKAGE := pingparsing
DOCS_DIR := docs
DOCS_BUILD_DIR := $(DOCS_DIR)/_build


.PHONY: build
build:
	@make clean
	@python setup.py sdist bdist_wheel
	@twine check dist/*
	@python setup.py clean --all
	ls -lh dist/*

.PHONY: check
check:
	python setup.py check
	codespell $(PACKAGE) docs examples test -q 2 --check-filenames --ignore-words-list followings
	travis lint
	pylama

.PHONY: clean
clean:
	@tox -e clean

.PHONY: docs
docs:
	@cd docs && ./update_command_help.py
	@python setup.py build_sphinx --source-dir=$(DOCS_DIR)/ --build-dir=$(DOCS_BUILD_DIR) --all-files

.PHONY: idocs
idocs:
	@pip install --upgrade .
	@make docs

.PHONY: fmt
fmt:
	@black $(CURDIR)
	@autoflake --in-place --recursive --remove-all-unused-imports --ignore-init-module-imports .
	@isort --apply --recursive

.PHONY: readme
readme:
	@cd $(DOCS_DIR); python make_readme.py

.PHONY: release
release:
	@tox -e release
	@make clean

.PHONY: setup
setup:
	@pip install --upgrade .[dev] tox
