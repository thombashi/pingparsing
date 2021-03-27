.PHONY: build
build:
	@make clean
	@tox -e build
	ls -lh dist/*

.PHONY: check
check:
	@-tox -e lint
	python3 -m pip check

.PHONY: clean
clean:
	@tox -e clean

.PHONY: docs
docs:
	@cd docs && ./update_command_help.py
	@tox -e docs

.PHONY: idocs
idocs:
	@python3 -m pip install --upgrade .
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
	@python setup.py release --sign
	@make clean

.PHONY: setup
setup:
	@python3 -m pip install --upgrade -e .[test] releasecmd tox
	python3 -m pip check
