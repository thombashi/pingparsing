PYTHON := python3


.PHONY: build
build: clean
	@tox -e build
	ls -lh dist/*

.PHONY: check
check:
	@-tox -e lint

.PHONY: clean
clean:
	@tox -e clean

.PHONY: docs
docs:
	@cd docs && ./update_command_help.py
	@tox -e docs

.PHONY: idocs
idocs:
	@$(PYTHON) -m pip install -q --disable-pip-version-check --upgrade .
	@make docs

.PHONY: fmt
fmt:
	@tox -e fmt

.PHONY: readme
readme:
	@cd docs && ./update_command_help.py
	@tox -e readme

.PHONY: release
release:
	@$(PYTHON) setup.py release --sign --search-dir pingparsing
	@make clean

.PHONY: setup
setup:
	@$(PYTHON) -m pip install -q --disable-pip-version-check --upgrade -e .[test] releasecmd tox
	@$(PYTHON) -m pip check
