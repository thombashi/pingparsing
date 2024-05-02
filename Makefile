PYTHON := python3


.PHONY: build
build: clean
	@$(PYTHON) -m tox -e build
	ls -lh dist/*

.PHONY: check
check:
	@$(PYTHON) -m tox -e lint

.PHONY: clean
clean:
	@$(PYTHON) -m tox -e clean

.PHONY: docs
docs:
	@cd docs && ./update_command_help.py
	@$(PYTHON) -m tox -e docs

.PHONY: idocs
idocs:
	@$(PYTHON) -m pip install -q --disable-pip-version-check --upgrade .
	@$(MAKE) docs

.PHONY: fmt
fmt:
	@$(PYTHON) -m tox -e fmt

.PHONY: readme
readme:
	@cd docs && ./update_command_help.py
	@$(PYTHON) -m tox -e readme

.PHONY: release
release:
	$(PYTHON) -m tox -e release
	$(MAKE) clean

.PHONY: setup-ci
setup-ci:
	$(PYTHON) -m pip install -q --disable-pip-version-check --upgrade pip
	$(PYTHON) -m pip install -q --disable-pip-version-check --upgrade tox

.PHONY: setup-dev
setup-dev: setup-ci
	$(PYTHON) -m pip install -q --disable-pip-version-check --upgrade -e .[test]
	$(PYTHON) -m pip check

.PHONY: test
test:
	$(PYTHON) -m tox -e py
